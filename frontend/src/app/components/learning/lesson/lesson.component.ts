import { CommonModule, Location } from '@angular/common';
import { Component } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { SUBJECTS } from '../learning-subjects.data';
import { LearningAtom, LearningTopic, Subject, LearningModule } from '../learning.models';
import { AuthService } from '../../../auth/auth.service';
import { FormsModule } from '@angular/forms';
import { environment } from '../../../../environments/environment';

type ViewState = 'video' | 'mode-select' | 'online-quiz' | 'results' | 'history';
type AttemptType = 'practice' | 'challenge';
type AttemptMode = 'online' | 'download';

@Component({
  selector: 'app-lesson',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './lesson.component.html',
  styleUrls: ['./lesson.component.scss']
})
export class LessonComponent {
  subject: Subject | undefined;
  module: LearningModule | undefined;
  topic: LearningTopic | undefined;
  currentLevel: LearningAtom | undefined;
  safeVideoUrl: SafeResourceUrl | null = null;
  isAdmin = false;

  // View state management
  viewState: ViewState = 'video';
  selectedAttemptType: AttemptType | null = null;
  selectedMode: AttemptMode | null = null;

  // Quiz state
  attemptId: string = '';
  questions: any[] = [];
  currentQuestionIndex = 0;
  answers: Record<string, string> = {};
  result: any = null;

  // History
  attemptHistory: any[] = [];

  readonly apiBase = environment.apiBaseUrl;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private location: Location,
    private sanitizer: DomSanitizer,
    private http: HttpClient,
    private auth: AuthService
  ) {
    this.isAdmin = auth.isAdmin();
    this.route.paramMap.subscribe(params => {
      const moduleId = params.get('moduleId');
      const topicId = params.get('topicId') || params.get('subskillId');
      const levelNum = parseInt(params.get('level') || '1');

      // Find subject, module, topic, and level
      for (const subj of SUBJECTS) {
        const mod = subj.modules.find(m => m.id === moduleId);
        if (mod) {
          this.subject = subj;
          this.module = mod;

          // Check if module has topics
          if (mod.topics) {
            this.topic = mod.topics.find(t => t.id === topicId);
            this.currentLevel = this.topic?.levels.find(l => l.level === levelNum);
          } else {
            // Direct atoms
            this.currentLevel = mod.atoms?.find(a => a.id === topicId);
          }
          break;
        }
      }

      if (!this.currentLevel) {
        this.router.navigate(['/learning']);
        return;
      }

      this.safeVideoUrl = this.sanitizer.bypassSecurityTrustResourceUrl(this.currentLevel.videoUrl);
      this.loadHistory();
    });
  }

  // Start practice or challenge - ONLINE ONLY (no download option)
  startAttempt(type: AttemptType): void {
    this.selectedAttemptType = type;
    this.selectedMode = 'online'; // Always online for lessons
    this.generateAttempt(); // Skip mode selection, go directly to quiz
  }

  // Select mode (online or download) - DEPRECATED for lessons
  selectMode(mode: AttemptMode): void {
    this.selectedMode = mode;
    this.generateAttempt();
  }

  // Generate attempt via API
  generateAttempt(): void {
    const userId = this.auth.getUserId();
    const isChallenge = this.selectedAttemptType === 'challenge';
    const payload = {
      user_id: userId,
      subject_id: this.subject?.id,
      module_id: this.module?.id,
      topic_id: this.topic?.id || this.currentLevel?.id,
      level: this.currentLevel?.level || 1,
      attempt_type: this.selectedAttemptType,
      mode: this.selectedMode,
      num_questions: isChallenge ? 10 : 5
    };

    this.http.post<any>(`${this.apiBase}/practice/generate`, payload).subscribe({
      next: (response) => {
        this.attemptId = response.attempt_id;

        if (this.selectedMode === 'online') {
          this.questions = response.questions;
          this.currentQuestionIndex = 0;
          this.answers = {};
          this.viewState = 'online-quiz';
        } else {
          // Download mode
          this.downloadPDFs();
          this.viewState = 'video';
          this.loadHistory();
        }
      },
      error: (err) => {
        console.error('Failed to generate attempt:', err);
        alert('Failed to generate practice. Please try again.');
      }
    });
  }

  // Download topic notes PDF (e.g. Karel notes)
  downloadNotes(): void {
    const topicId = this.currentLevel?.notesTopicId;
    if (!topicId) return;
    window.open(`${this.apiBase}/learning/notes/${topicId}`, '_blank');
  }

  // Download PDFs
  downloadPDFs(): void {
    const studentName = this.auth.getCurrentUser()?.name || localStorage.getItem('username') || '';
    const encodedName = encodeURIComponent(studentName);
    // `question-pdf` now returns a combined file (question paper + answer sheet)
    window.open(`${this.apiBase}/practice/${this.attemptId}/question-pdf?student_name=${encodedName}`, '_blank');
  }

  // Answer question
  selectAnswer(option: string): void {
    const qNum = this.questions[this.currentQuestionIndex].question_number;
    this.answers[`q${qNum}`] = option;
  }

  // Navigate questions
  nextQuestion(): void {
    if (this.currentQuestionIndex < this.questions.length - 1) {
      this.currentQuestionIndex++;
    }
  }

  prevQuestion(): void {
    if (this.currentQuestionIndex > 0) {
      this.currentQuestionIndex--;
    }
  }

  // Submit online quiz
  submitQuiz(): void {
    this.http.post<any>(`${this.apiBase}/practice/${this.attemptId}/submit`, {
      answers: this.answers
    }).subscribe({
      next: (response) => {
        this.result = response;
        this.viewState = 'results';
        this.loadHistory();
      },
      error: (err) => {
        console.error('Failed to submit quiz:', err);
        alert('Failed to submit answers. Please try again.');
      }
    });
  }

  // Load attempt history
  loadHistory(): void {
    const userId = this.auth.getUserId();
    this.http.get<any[]>(`${this.apiBase}/practice/history/${userId}`, {
      params: { subject_id: this.subject?.id || '' }
    }).subscribe({
      next: (history) => {
        this.attemptHistory = history.filter(h =>
          h.module_id === this.module?.id &&
          (h.topic_id === this.topic?.id || h.topic_id === this.currentLevel?.id)
        );
      },
      error: (err) => console.error('Failed to load history:', err)
    });
  }

  // View history
  showHistory(): void {
    this.viewState = 'history';
  }

  // Restart - go back to video
  restartLesson(): void {
    this.viewState = 'video';
    this.selectedAttemptType = null;
    this.selectedMode = null;
    this.result = null;
    this.questions = [];
    this.answers = {};
  }

  // Check if next level exists
  completeLevel(): void {
    if (this.topic && this.currentLevel) {
      const nextLevel = this.topic.levels.find(l => l.level === this.currentLevel!.level + 1);
      if (nextLevel) {
        this.router.navigate(['/learning', this.module?.id, this.topic.id, 'level', nextLevel.level]);
      } else {
        alert('Congratulations! You completed all levels for ' + this.topic.name);
        this.router.navigate(['/learning']);
      }
    }
  }

  goBack(): void {
    // If in any practice/challenge flow, return to lesson view
    if (this.viewState === 'results' || this.viewState === 'history' || this.viewState === 'online-quiz') {
      this.restartLesson(); // Go back to lesson with video and notes
      return;
    }

    // If topic has levels, go to the previous level first.
    if (this.topic && this.currentLevel && this.currentLevel.level > 1) {
      this.router.navigate([
        '/learning',
        this.module?.id,
        this.topic.id,
        'level',
        this.currentLevel.level - 1
      ]);
      return;
    }

    // Otherwise return to previous page in app history.
    if (window.history.length > 1) {
      this.location.back();
      return;
    }

    // Safe fallback when there is no usable history.
    if (this.module?.id) {
      this.router.navigate(['/learning', this.module.id]);
      return;
    }

    this.router.navigate(['/learning']);
  }

  getBackButtonLabel(): string {
    if (this.viewState === 'results' || this.viewState === 'history' || this.viewState === 'online-quiz') {
      return '← Back to Lesson';
    }
    if (this.topic && this.currentLevel && this.currentLevel.level > 1) {
      return `← Back to Level ${this.currentLevel.level - 1}`;
    }
    if (this.module?.name) {
      return `← Back to ${this.module.name}`;
    }
    return '← Back';
  }

  getSimpleDefinition(): string {
    if (!this.currentLevel) return '';

    if (this.module?.id === 'binary-number-system') {
      return 'A binary number system is a way of writing numbers using only two digits: 0 and 1. Computers use binary to store and process all data.';
    }
    if (this.module?.id === 'probability') {
      return 'Probability tells us how likely something is to happen. It is written between 0 and 1, where 0 means impossible and 1 means certain.';
    }
    if (this.module?.id === 'four-operations') {
      return `${this.topic?.name || this.currentLevel.name} is a core arithmetic skill used to solve number problems accurately and quickly.`;
    }
    if (this.module?.id === 'fractions-decimals') {
      return 'Fractions and decimals are two ways to represent parts of a whole, and they help us compare and calculate quantities.';
    }

    if (this.currentLevel?.id === 'python-with-karel') {
      return 'Karel is a robot that lives on a grid world. You give it commands like move(), turn_left(), and put_beeper() to make it do things. It is the easiest way to start programming!';
    }

    return this.firstSentence(this.currentLevel.teachingNotes) || this.currentLevel.summary;
  }

  getRealLifeUses(): string[] {
    if (this.module?.id === 'binary-number-system') {
      return [
        'Mobile phones and laptops store photos, videos, and messages in binary.',
        'QR codes and digital barcodes are read by systems that convert patterns into binary data.',
        'Games and apps run because instructions are processed as binary machine code.'
      ];
    }
    if (this.module?.id === 'probability') {
      return [
        'Weather forecasts use probability (for example, 70% chance of rain).',
        'Sports predictions use probability based on past matches.',
        'Games with dice, cards, and spinners all use probability ideas.'
      ];
    }
    if (this.module?.id === 'four-operations') {
      return [
        'Shopping totals and change calculations.',
        'Splitting food or money equally between people.',
        'Working out travel time, distance, and speed.'
      ];
    }
    if (this.module?.id === 'fractions-decimals') {
      return [
        'Recipes use fractions for ingredient amounts.',
        'Money uses decimals (for example, £3.75).',
        'Measurements in science and design use fractions and decimals.'
      ];
    }

    if (this.currentLevel?.id === 'python-with-karel') {
      return [
        'Game developers write code to move characters — just like you move Karel!',
        'Warehouse robots follow step-by-step instructions to pick and place items.',
        'Self-driving cars use simple commands (go forward, turn, stop) to navigate roads.',
        'Factory assembly lines use robot programs to build products automatically.'
      ];
    }

    return [
      'Used in school tests and problem-solving tasks.',
      'Helps make better decisions in daily life situations.',
      'Builds strong logic and number confidence for future topics.'
    ];
  }

  getWorkedExamples(): string[] {
    if (this.module?.id === 'binary-number-system') {
      return [
        'Example 1: 0101 in binary = 4 + 1 = 5 in denary.',
        'Example 2: 1010 + 0011 = 1101 (binary addition with carrying).'
      ];
    }
    if (this.module?.id === 'probability') {
      return [
        'Example 1: A fair coin has 2 outcomes, so P(Heads) = 1/2.',
        'Example 2: A bag has 3 red and 2 blue counters. P(blue) = 2/5.'
      ];
    }
    if (this.topic?.id === 'addition') {
      return [
        'Example 1: 248 + 367 = 615 using column addition.',
        'Example 2: 1,209 + 586 = 1,795 by lining up place values.'
      ];
    }
    if (this.topic?.id === 'subtraction') {
      return [
        'Example 1: 503 - 178 = 325 using borrowing.',
        'Example 2: 1,000 - 457 = 543 by regrouping correctly.'
      ];
    }
    if (this.topic?.id === 'multiplication') {
      return [
        'Example 1: 36 x 7 = 252 using short multiplication.',
        'Example 2: 24 x 13 = 312 using partitioning or long multiplication.'
      ];
    }
    if (this.topic?.id === 'division') {
      return [
        'Example 1: 84 ÷ 6 = 14.',
        'Example 2: 95 ÷ 4 = 23 remainder 3.'
      ];
    }

    if (this.currentLevel?.id === 'python-with-karel') {
      return [
        'Example 1 — Move Karel forward 3 steps: write move() three times, one per line. Karel moves one square each time.',
        'Example 2 — Place a ball and move on: write put_beeper() to drop a ball on the current square, then move() to step forward.',
        'Example 3 — Turn Karel right: because Karel only knows turn_left(), call turn_left() three times in a row to face right.'
      ];
    }

    return [
      `Example 1: ${this.currentLevel?.summary || 'Use the method step by step on a simple question.'}`,
      'Example 2: Try a slightly harder question and check your answer carefully.'
    ];
  }

  getLessonSummary(): string[] {
    const points: string[] = [];
    points.push(`You now know the main idea of ${this.topic?.name || this.currentLevel?.name || 'this topic'}.`);
    if (this.currentLevel?.assessmentCriteria) {
      points.push(this.currentLevel.assessmentCriteria);
    }
    points.push('Next step: apply this in timed practice and review mistakes.');
    return points;
  }

  getMiniTask(): string[] {
    if (this.module?.id === 'binary-number-system') {
      return [
        'Convert 0110 (binary) to denary.',
        'Convert denary 9 to binary.',
        'Add 0101 + 0011 in binary.'
      ];
    }
    if (this.module?.id === 'probability') {
      return [
        'A spinner has 8 equal sections, 3 are red. Find P(red).',
        'A die is rolled once. Find P(not 6).',
        'A bag has 5 green and 5 yellow counters. Find P(green).'
      ];
    }
    if (this.topic?.id === 'addition') {
      return ['473 + 289', '1,248 + 367', '5,906 + 2,189'];
    }
    if (this.topic?.id === 'subtraction') {
      return ['904 - 378', '1,200 - 467', '5,000 - 2,759'];
    }
    if (this.topic?.id === 'multiplication') {
      return ['38 x 6', '47 x 12', '125 x 8'];
    }
    if (this.topic?.id === 'division') {
      return ['96 ÷ 8', '144 ÷ 12', '117 ÷ 5 (with remainder)'];
    }

    if (this.currentLevel?.id === 'python-with-karel') {
      return [
        'Write a program that moves Karel forward 2 squares.',
        'Write a program that makes Karel turn right (hint: 3 × turn_left).',
        'Write a program that places a beeper, moves forward, then places another beeper.'
      ];
    }

    return [
      'Solve one easy question on this topic.',
      'Solve one medium question on this topic.',
      'Explain your method in one sentence.'
    ];
  }

  getRegularStrategies(): string[] {
    const list = this.currentLevel?.teachingStrategies || [];
    return list.filter(s => !this.isTaggedNote(s));
  }

  getReferenceNotes(): string[] {
    const list = this.currentLevel?.teachingStrategies || [];
    return list
      .filter(s => s.startsWith('Reference:'))
      .map(s => this.stripPrefix(s, 'Reference:'));
  }

  getOnlineNotes(): string[] {
    const list = this.currentLevel?.teachingStrategies || [];
    return list
      .filter(s => s.startsWith('Online:'))
      .map(s => this.stripPrefix(s, 'Online:'));
  }

  getQuickNotes(): string[] {
    const list = this.currentLevel?.teachingStrategies || [];
    return list
      .filter(s => s.startsWith('Quick note:'))
      .map(s => this.stripPrefix(s, 'Quick note:'));
  }

  getTaggedNotes(): string[] {
    const list = this.currentLevel?.teachingStrategies || [];
    return list.filter(s => this.isTaggedNote(s));
  }

  private isTaggedNote(value: string): boolean {
    return value.startsWith('Reference:') || value.startsWith('Online:') || value.startsWith('Quick note:');
  }

  private stripPrefix(value: string, prefix: string): string {
    return value.startsWith(prefix) ? value.slice(prefix.length).trim() : value.trim();
  }

  getExplanationSteps(explanation: string): string[] {
    if (!explanation) return [];
    // Split on '. ' or '.\n' keeping meaningful sentences, filter blanks
    return explanation
      .split(/(?<=\.)\s+/)
      .map(s => s.trim())
      .filter(s => s.length > 4);
  }

  private firstSentence(text: string): string {
    if (!text) return '';
    const cleaned = text.replace(/\s+/g, ' ').trim();
    const match = cleaned.match(/.+?[.!?](\s|$)/);
    return match ? match[0].trim() : cleaned;
  }

  scrollHelpSheet(container: HTMLElement, direction: 'left' | 'right'): void {
    const delta = direction === 'left' ? -container.clientWidth * 0.85 : container.clientWidth * 0.85;
    container.scrollBy({ left: delta, behavior: 'smooth' });
  }
}
