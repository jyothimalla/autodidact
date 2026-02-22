import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../auth/auth.service';
import { environment } from '../../../environments/environment';

interface McqQuestion {
  question_number: number;
  question_id: string;
  module_id: string;
  question: string;
  options: { A: string; B: string; C: string; D: string };
  correct_option?: string;
  correct_answer?: string;
  explanation?: string;
}

interface ReviewItem {
  question_number: number;
  question: string;
  options: { A: string; B: string; C: string; D: string };
  your_answer: string;
  correct_option: string;
  correct_answer: string;
  explanation: string;
  is_correct: boolean;
  expanded?: boolean;  // For UI state
}

interface ExamResult {
  score: number;
  total: number;
  percentage: number;
  passed: boolean;
  time_taken: number;
  breakdown: { label: string; score: number; total: number }[];
  review: ReviewItem[];
}

interface SectionSummaryItem {
  section_name: string;
  num_questions: number;
  suggested_minutes: number;
}

@Component({
  selector: 'app-mock-test',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './mock-test.component.html',
  styleUrls: ['./mock-test.component.scss'],
})
export class MockTestComponent implements OnInit, OnDestroy {
  state: 'welcome' | 'loading' | 'test-ready' | 'exam' | 'submission' | 'submitted' = 'welcome';

  testId = '';
  questions: McqQuestion[] = [];
  answers: Record<string, string> = {};   // { q1: 'A', q2: 'C', ... }
  currentIndex = 0;
  errorMessage = '';
  showReview = false;
  result: ExamResult | null = null;
  examStyle: 'standard' | 'cem' | 'english' = 'standard';
  targetYear: 'year4' | 'year5' = 'year4';
  sectionSummary: SectionSummaryItem[] = [];

  // Practice papers and generated tests
  practiceTests: Array<{paper_number: number, title: string}> = [];
  myGeneratedTests: Array<{test_id: string, created_at: string}> = [];

  // Download and submission
  showDownloadOptions = false;
  uploadFile: File | null = null;
  manualAnswers: Record<string, string> = {};
  explicitlyUnanswered = new Set<string>();

  // Timer
  timeLeft = 3600;   // seconds
  private timerHandle: ReturnType<typeof setInterval> | null = null;
  showHelpSheet = false;
  hintOverlayOpen = false;
  hintSkippedQuestionIds = new Set<string>();

  private readonly apiBase = environment.apiBaseUrl;

  readonly optionLabels: ('A' | 'B' | 'C' | 'D')[] = ['A', 'B', 'C', 'D'];

  constructor(
    private http: HttpClient,
    private auth: AuthService,
    public router: Router,
    private route: ActivatedRoute,
  ) {}

  // Submission page state
  submissionQuestions: McqQuestion[] = [];
  loadingSubmissionQuestions = false;

  ngOnInit(): void {
    // Check if we're on the submission route (from QR code)
    const testId = this.route.snapshot.paramMap.get('testId');
    if (testId) {
      this.testId = testId;
      this.state = 'submission';
      this.loadSubmissionQuestions();
    } else {
      this.loadPracticePapers();
      this.loadMyGeneratedTests();
    }
  }

  loadSubmissionQuestions(): void {
    if (!this.testId) return;
    this.loadingSubmissionQuestions = true;
    this.http.get<any>(`${this.apiBase}/test/${this.testId}`).subscribe({
      next: (data) => {
        this.submissionQuestions = data.questions;
        this.loadingSubmissionQuestions = false;
        // Initialize manual answers with empty strings
        for (const q of this.submissionQuestions) {
          this.manualAnswers[q.question_id] = '';
        }
      },
      error: () => {
        this.errorMessage = 'Failed to load test questions.';
        this.loadingSubmissionQuestions = false;
      }
    });
  }

  selectManualAnswer(questionId: string, answer: string): void {
    this.manualAnswers[questionId] = answer;
    if (answer === '') {
      this.explicitlyUnanswered.add(questionId);
    } else {
      this.explicitlyUnanswered.delete(questionId);
    }
  }

  getManualAnsweredCount(): number {
    return Object.values(this.manualAnswers).filter(a => a !== '').length;
  }

  get userId(): number {
    return this.auth.getUserId() ?? 0;
  }

  // ── Practice Papers & Generated Tests ──────────────────────────────────

  loadPracticePapers(): void {
    this.http.get<any[]>(`${this.apiBase}/grammar/papers`).subscribe({
      next: (papers) => {
        this.practiceTests = papers;
      },
      error: () => {}
    });
  }

  loadMyGeneratedTests(): void {
    const userId = this.userId;
    if (!userId) return;

    this.http.get<any[]>(`${this.apiBase}/test/generated/${userId}`).subscribe({
      next: (tests) => {
        this.myGeneratedTests = tests.map((t: any) => ({
          test_id: t.test_id,
          created_at: t.created_at
        }));
      },
      error: () => {}
    });
  }

  selectPracticeTest(paperNumber: number, mode: 'online' | 'download' = 'online'): void {
    if (mode === 'download') {
      this.downloadPracticePaperPDF(paperNumber);
      return;
    }

    this.http.get<any>(`${this.apiBase}/grammar/papers/${paperNumber}/questions`).subscribe({
      next: (data) => {
        this.questions = data.questions;
        this.testId = `practice_${paperNumber}`;
        this.state = 'exam';
        this.startTimer();
      },
      error: () => {
        this.errorMessage = 'Failed to load practice paper. Please try again.';
      }
    });
  }

  downloadPracticePaperPDF(paperNumber: number): void {
    // Get student name from auth service or prompt
    const studentName = this.auth.getCurrentUser()?.name || prompt('Enter your name for the test paper:') || '';
    const url = `${this.apiBase}/grammar/papers/${paperNumber}/combined-pdf?student_name=${encodeURIComponent(studentName)}`;
    window.open(url, '_blank');
  }

  // ── Download & Submission Methods ──────────────────────────────────────

  attemptOnline(): void {
    this.showHelpSheet = false;
    this.hintOverlayOpen = false;
    this.hintSkippedQuestionIds.clear();
    // If questions are already loaded (from generate), go straight to exam
    if (this.questions.length > 0) {
      this.state = 'exam';
      this.startTimer();
      return;
    }

    // Otherwise load questions from API first
    this.state = 'loading';
    this.http.get<any>(`${this.apiBase}/test/${this.testId}`).subscribe({
      next: (data) => {
        this.questions = data.questions;
        this.sectionSummary = data.section_summary || [];
        this.examStyle = data.exam_style || this.examStyle;
        this.targetYear = data.target_year || this.targetYear;
        this.timeLeft = data.time_limit_seconds ?? 3600;
        this.answers = {};
        this.currentIndex = 0;
        this.state = 'exam';
        this.startTimer();
      },
      error: () => {
        this.errorMessage = 'Failed to load test questions. Please try again.';
        this.state = 'welcome';
      }
    });
  }

  downloadQuestionPDF(): void {
    const studentName = this.auth.getCurrentUser()?.name || localStorage.getItem('username') || '';
    window.open(`${this.apiBase}/test/${this.testId}/question-pdf?student_name=${encodeURIComponent(studentName)}`, '_blank');
  }

  downloadAnswerSheetPDF(): void {
    const studentName = this.auth.getCurrentUser()?.name || localStorage.getItem('username') || '';
    window.open(`${this.apiBase}/test/${this.testId}/answer-sheet-pdf?student_name=${encodeURIComponent(studentName)}`, '_blank');
  }

  downloadBothPDFs(): void {
    const studentName = this.auth.getCurrentUser()?.name || localStorage.getItem('username') || '';
    const encodedName = encodeURIComponent(studentName);
    // `question-pdf` now returns a combined file (question paper + answer sheet)
    window.open(`${this.apiBase}/test/${this.testId}/question-pdf?student_name=${encodedName}`, '_blank');
  }

  onFileSelected(event: any): void {
    this.uploadFile = event.target.files[0];
  }

  submitUploadedAnswers(): void {
    if (!this.uploadFile) return;

    const formData = new FormData();
    formData.append('file', this.uploadFile);
    formData.append('user_id', this.userId.toString());

    this.http.post<ExamResult>(`${this.apiBase}/test/${this.testId}/check-upload`, formData).subscribe({
      next: (result) => {
        // Initialize expanded property for each review item
        result.review.forEach(item => item.expanded = false);
        this.result = result;
        this.state = 'submitted';
      },
      error: () => {
        this.errorMessage = 'Failed to process upload. Please try again.';
      }
    });
  }

  submitManualAnswers(): void {
    const userId = this.userId;
    this.http.post<ExamResult>(`${this.apiBase}/test/${this.testId}/check-typed`, {
      user_id: userId,
      answers: this.manualAnswers
    }).subscribe({
      next: (result) => {
        // Initialize expanded property for each review item
        result.review.forEach(item => item.expanded = false);
        this.result = result;
        this.state = 'submitted';
      },
      error: () => {
        this.errorMessage = 'Failed to submit answers. Please try again.';
      }
    });
  }

  // ── Timer ──────────────────────────────────────────────────────────────

  get timerDisplay(): string {
    const m = Math.floor(this.timeLeft / 60).toString().padStart(2, '0');
    const s = (this.timeLeft % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }

  get timerClass(): string {
    if (this.timeLeft <= 300) return 'timer-red';
    if (this.timeLeft <= 600) return 'timer-orange';
    return '';
  }

  private startTimer(): void {
    this.timerHandle = setInterval(() => {
      this.timeLeft--;
      if (this.timeLeft <= 0) {
        this.submitExam(true);
      }
    }, 1000);
  }

  private stopTimer(): void {
    if (this.timerHandle) {
      clearInterval(this.timerHandle);
      this.timerHandle = null;
    }
  }

  // ── Navigation ─────────────────────────────────────────────────────────

  get currentQuestion(): McqQuestion {
    return this.questions[this.currentIndex];
  }

  get answeredCount(): number {
    return Object.keys(this.answers).length;
  }

  goTo(index: number): void {
    if (index >= 0 && index < this.questions.length) {
      this.currentIndex = index;
    }
  }

  next(): void { this.goTo(this.currentIndex + 1); }
  prev(): void { this.goTo(this.currentIndex - 1); }

  selectAnswer(option: string): void {
    this.answers[this.currentQuestion.question_id] = option;
  }

  get moduleLabelForHelp(): string {
    const label = this.currentQuestion?.module_id || '';
    return label.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  }

  openHelpVideo(): void {
    const module = this.currentQuestion?.module_id;
    const byModule: Record<string, string> = {
      'four-operations': 'https://www.youtube.com/watch?v=NybHckSEQBI',
      'fractions-decimals': 'https://www.youtube.com/watch?v=tDQipFjAoT8',
      'ratios': 'https://www.youtube.com/watch?v=GQ5vWUh6L3g',
      'percentages': 'https://www.youtube.com/watch?v=JeVSmq1Nrpw',
      'verbal-reasoning': 'https://www.youtube.com/watch?v=KD38vC6-dCM',
      'non-verbal-reasoning': 'https://www.youtube.com/watch?v=qn2F6z4Lw7Q',
      'english-cem': 'https://www.youtube.com/watch?v=6nqH6iM14sM',
      'grammar': 'https://www.youtube.com/watch?v=N5fyb6n3AAE',
      'comprehension': 'https://www.youtube.com/watch?v=V8f1UBCDgJ0',
      'binary-systems': 'https://www.youtube.com/watch?v=1-YMkNd3Fx0',
      'binary-hex-conversions-addition': 'https://www.youtube.com/watch?v=1-YMkNd3Fx0',
      'binary-shifts': 'https://www.youtube.com/watch?v=1-YMkNd3Fx0',
      'python-basics': 'https://www.youtube.com/watch?v=rfscVS0vtbw',
      'volumes': 'https://www.youtube.com/watch?v=6mWN6Yb2-N0',
    };
    const fallback = `https://www.youtube.com/results?search_query=${encodeURIComponent(this.moduleLabelForHelp + ' lesson for kids')}`;
    window.open(byModule[module || ''] || fallback, '_blank');
  }

  toggleHelpSheet(): void {
    this.showHelpSheet = !this.showHelpSheet;
  }

  get helpSheetIntro(): string {
    const m = this.currentQuestion?.module_id || '';
    if (m.includes('binary')) return 'Use place values (128, 64, 32, 16, 8, 4, 2, 1). For hex, split binary into nibbles.';
    if (m.includes('english') || m.includes('grammar') || m.includes('comprehension')) return 'Read the full sentence first, eliminate wrong options, then choose the best-fit answer.';
    if (m.includes('verbal')) return 'Find one clear rule, test it, then apply exactly the same rule to the missing part.';
    if (m.includes('non-verbal') || m.includes('nvr')) return 'Track one visual rule at a time: rotation, shape count, shading, or symmetry.';
    return 'Break the problem into short steps, estimate quickly, then check if your final answer matches the options.';
  }

  openSkipHint(): void {
    this.hintOverlayOpen = true;
  }

  closeSkipHint(): void {
    this.hintOverlayOpen = false;
  }

  skipToExplanationAndNext(): void {
    const qid = this.currentQuestion?.question_id;
    if (qid) this.hintSkippedQuestionIds.add(qid);
    this.hintOverlayOpen = false;
    if (this.currentIndex < this.questions.length - 1) this.next();
  }

  questionStatus(q: McqQuestion): 'answered' | 'current' | 'unanswered' {
    if (q.question_number - 1 === this.currentIndex) return 'current';
    return this.answers[q.question_id] ? 'answered' : 'unanswered';
  }

  // ── Exam lifecycle ─────────────────────────────────────────────────────

  startExam(): void {
    this.errorMessage = '';
    this.showHelpSheet = false;
    this.hintOverlayOpen = false;
    this.hintSkippedQuestionIds.clear();
    this.state = 'loading';

    this.http.post<any>(`${this.apiBase}/test/generate`, {
      user_id: this.userId,
      difficulty: 'mixed',
      exam_style: this.examStyle,
      target_year: this.targetYear,
    }).subscribe({
      next: (res) => {
        this.testId = res.test_id;
        this.questions = res.questions;
        this.sectionSummary = res.section_summary || [];
        this.examStyle = res.exam_style || this.examStyle;
        this.targetYear = res.target_year || this.targetYear;
        this.timeLeft = res.time_limit_seconds ?? 3600;
        this.state = 'test-ready';
        this.showDownloadOptions = true;
      },
      error: (err) => {
        this.errorMessage = err?.error?.detail ?? 'Failed to generate exam. Please try again.';
        this.state = 'welcome';
      },
    });
  }

  submitExam(autoSubmit = false): void {
    if (!autoSubmit) {
      const unanswered = this.questions.length - this.answeredCount;
      if (unanswered > 0) {
        const ok = confirm(`You have ${unanswered} unanswered question(s). Submit anyway?`);
        if (!ok) return;
      }
    }

    this.stopTimer();
    const timeTaken = 3600 - this.timeLeft;

    this.http.post<ExamResult>(`${this.apiBase}/test/${this.testId}/submit`, {
      user_id: this.userId,
      answers: this.answers,
      time_taken: timeTaken,
    }).subscribe({
      next: (res) => {
        // Initialize expanded property for each review item
        res.review.forEach(item => item.expanded = false);
        this.result = res;
        this.state = 'submitted';
      },
      error: () => {
        this.errorMessage = 'Failed to submit. Please try again.';
        this.startTimer();   // resume timer on failure
      },
    });
  }

  goBackFromExam(): void {
    const confirmed = confirm('Are you sure you want to exit the test? Your answers will not be saved.');
    if (confirmed) {
      this.stopTimer();
      this.answers = {};
      this.state = 'test-ready';
    }
  }

  restartExam(): void {
    this.stopTimer();
    this.testId = '';
    this.questions = [];
    this.answers = {};
    this.currentIndex = 0;
    this.result = null;
    this.showReview = false;
    this.sectionSummary = [];
    this.timeLeft = 3600;
    this.showHelpSheet = false;
    this.hintOverlayOpen = false;
    this.hintSkippedQuestionIds.clear();
    this.state = 'welcome';
  }

  ngOnDestroy(): void {
    this.stopTimer();
  }

  get styleInstructionTitle(): string {
    if (this.examStyle === 'cem') return 'CEM Blueprint Instructions';
    if (this.examStyle === 'english') return 'English Entrance Instructions';
    return 'Standard Mock Instructions';
  }

  get styleInstructions(): string[] {
    if (this.examStyle === 'cem') {
      return [
        'Work section by section using the suggested minutes shown below.',
        'If a question takes too long, mark and move on; return if time remains.',
        'Expect a mixed paper across numerical, verbal and logic sections.',
      ];
    }
    if (this.examStyle === 'english') {
      return [
        `This paper targets ${this.targetYear === 'year5' ? 'Year 5' : 'Year 4'} grammar-school English preparation.`,
        'Focus on vocabulary, cloze, grammar and punctuation accuracy.',
        'Use section timings to maintain pace and avoid spending too long on one item.',
      ];
    }
    return [
      'This is the default mixed mathematics mock with one overall 60-minute timing.',
      'Work steadily and focus on accuracy across all questions.',
    ];
  }
}
