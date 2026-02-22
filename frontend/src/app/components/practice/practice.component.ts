import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../auth/auth.service';
import { environment } from '../../../environments/environment';
import { SUBJECTS as LEARNING_SUBJECTS } from '../learning/learning-subjects.data';

interface Subject {
  id: string;
  name: string;
  icon: string;
  topics: Topic[];
}

interface Topic {
  id: string;
  name: string;
  backendId: string;
  supported: boolean;
}

interface GeneratedPaper {
  paper_id: string;
  subject_id: string;
  topic_id: string;
  topic_name: string;
  num_questions: number;
  difficulty: string;
  created_at: string;
  status: string;
  score?: number;
  percentage?: number;
}

@Component({
  selector: 'app-practice',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './practice.component.html',
  styleUrls: ['./practice.component.scss']
})
export class PracticeComponent implements OnInit {
  // The 4 core grammar school subjects shown as quick-start cards
  readonly featuredSubjects = [
    { id: 'maths', name: 'Maths', icon: '🔢', description: 'Arithmetic, fractions, algebra & more' },
    { id: 'english', name: 'English', icon: '📚', description: 'Grammar, comprehension & vocabulary' },
    { id: 'verbal-reasoning', name: 'Verbal Reasoning', icon: '🗣️', description: 'Patterns, analogies & logic' },
    { id: 'non-verbal-reasoning', name: 'Non-Verbal Reasoning', icon: '🧩', description: 'Shapes, sequences & spatial reasoning' },
  ];

  // Mapping from learning module IDs to backend generator IDs (where they differ)
  private readonly backendIdMap: Record<string, string> = {
    'word-problems': 'multi-step-word-problems',
    'speed-calculation': 'speed-based-calculation',
    'number-puzzles': 'logical-number-puzzles'
  };

  // Module IDs that the backend MCQ generator currently supports
  private readonly supportedModules = new Set([
    'four-operations', 'fractions-decimals', 'ratios', 'percentages',
    'multi-step-word-problems', 'mental-arithmetic', 'speed-based-calculation',
    'logical-number-puzzles',
    'probability', 'algebra', 'perimeter-area', 'angles',
    'coordinate-geometry', 'volumes', 'verbal-reasoning',
    'verbal-reasoning-level-1', 'verbal-reasoning-level-2',
    'verbal-reasoning-cem-vocab-codes', 'verbal-reasoning-cem-sequences-analogies',
    'non-verbal-reasoning', 'nvr-cem-pattern-matrices', 'nvr-cem-rotations-reflections',
    'nvr-cem-odd-one-out', 'nvr-cem-3d-nets',
    'grammar', 'punctuation', 'synonyms', 'antonyms', 'comprehension',
    'creative-writing', 'narrative-writing', 'non-chronological-report',
    'intro-it-safety', 'spreadsheets-basics', 'scratch-programming', 'block-programming',
    'binary-systems', 'binary-shifts', 'logic-gates', 'circuit-design',
    'python-basics', 'python-control', 'python-functions', 'python-data-structures',
    'computer-architecture', 'memory-storage', 'data-representation', 'input-output',
    'db-basics', 'db-sql-queries', 'os-basics', 'network-basics',
    'internet-protocols', 'web-basics', 'ds-arrays-lists', 'ds-stack-queue',
    'algo-searching', 'algo-sorting'
  ]);

  subjects: Subject[] = [];

  questionOptions = [5, 10, 15, 20];
  difficultyOptions = ['Easy', 'Medium', 'Hard', 'Mixed'];
  timeLimitOptions = [
    { questions: 5,  time: 5  },
    { questions: 5,  time: 10 },
    { questions: 10, time: 10 },
    { questions: 10, time: 15 },
    { questions: 15, time: 15 },
    { questions: 15, time: 20 },
    { questions: 20, time: 20 },
    { questions: 20, time: 30 }
  ];

  // Form state
  selectedSubject: string = '';
  selectedTopic: string = '';
  numQuestions: number = 10;
  difficulty: string = 'Mixed';
  timeLimit: number = 10;

  // UI state
  state: 'form' | 'paper-ready' = 'form';
  availableTopics: Topic[] = [];
  generatedPapers: GeneratedPaper[] = [];
  generating = false;
  readyPaperId = '';
  readyPaperName = '';

  private readonly apiBase = environment.apiBaseUrl;

  constructor(
    private router: Router,
    private http: HttpClient,
    private auth: AuthService
  ) {}

  ngOnInit(): void {
    this.subjects = LEARNING_SUBJECTS.map(s => ({
      id: s.id,
      name: s.name,
      icon: s.icon,
      topics: s.modules.flatMap(m => {
        const useAtomsAsTopics =
          (s.id === 'verbal-reasoning' || s.id === 'non-verbal-reasoning' || s.id === 'computers')
          && Array.isArray((m as any).atoms)
          && (m as any).atoms.length > 0;

        if (useAtomsAsTopics) {
          return (m as any).atoms.map((a: any) => {
            const backendId = this.backendIdMap[a.id] || a.id;
            return {
              id: a.id,
              name: a.name,
              backendId,
              supported: this.supportedModules.has(backendId)
            };
          });
        }

        const backendId = this.backendIdMap[m.id] || m.id;
        return [{
          id: m.id,
          name: m.name,
          backendId,
          supported: this.supportedModules.has(backendId)
        }];
      })
    }));
    this.loadGeneratedPapers();
  }

  // ── Subject quick-start ─────────────────────────────────────────────────
  quickStartSubject(subjectId: string): void {
    this.selectedSubject = subjectId;
    this.onSubjectChange();
    setTimeout(() => {
      document.getElementById('generation-form')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 50);
  }

  // ── Papers grouped by subject ──────────────────────────────────────────
  getSubjectPapers(subjectId: string): GeneratedPaper[] {
    return this.generatedPapers.filter(p => p.subject_id === subjectId);
  }

  get hasAnyPapers(): boolean {
    return this.generatedPapers.length > 0;
  }

  get otherSubjectPapers(): GeneratedPaper[] {
    const featuredIds = new Set(this.featuredSubjects.map(s => s.id));
    return this.generatedPapers.filter(p => !featuredIds.has(p.subject_id));
  }

  // ── Form helpers ───────────────────────────────────────────────────────
  onSubjectChange(): void {
    const subject = this.subjects.find(s => s.id === this.selectedSubject);
    this.availableTopics = subject ? subject.topics : [];
    this.selectedTopic = '';
  }

  onQuestionCountChange(): void {
    const options = this.timeLimitOptions.filter(opt => opt.questions === this.numQuestions);
    if (options.length > 0) this.timeLimit = options[0].time;
  }

  getTimeLimitOptions(): number[] {
    return this.timeLimitOptions
      .filter(opt => opt.questions === this.numQuestions)
      .map(opt => opt.time);
  }

  canGeneratePaper(): boolean {
    if (!(this.selectedSubject && this.selectedTopic && this.numQuestions && this.difficulty)) {
      return false;
    }
    const topic = this.availableTopics.find(t => t.id === this.selectedTopic);
    return !!topic?.supported;
  }

  generatePaper(): void {
    if (!this.canGeneratePaper()) {
      alert('Please fill in all fields and select a supported topic');
      return;
    }

    this.generating = true;
    const userId = this.auth.getUserId();
    const topic = this.availableTopics.find(t => t.id === this.selectedTopic);
    const moduleId = topic?.backendId || this.selectedTopic;

    const payload = {
      user_id: userId,
      subject_id: this.selectedSubject,
      module_id: moduleId,
      num_questions: this.numQuestions,
      difficulty: this.difficulty.toLowerCase(),
      time_limit: this.timeLimit
    };

    this.http.post<any>(`${this.apiBase}/practice/generate`, payload).subscribe({
      next: (response) => {
        this.generating = false;
        const topicName = this.availableTopics.find(t => t.id === this.selectedTopic)?.name || this.selectedTopic;
        this.generatedPapers.unshift({
          paper_id: response.paper_id,
          subject_id: this.selectedSubject,
          topic_id: this.selectedTopic,
          topic_name: topicName,
          num_questions: this.numQuestions,
          difficulty: this.difficulty,
          created_at: new Date().toISOString(),
          status: 'Not Attempted'
        });
        this.readyPaperId = response.paper_id;
        this.readyPaperName = topicName;
        this.state = 'paper-ready';
      },
      error: (err) => {
        console.error('Failed to generate paper:', err);
        alert('Failed to generate practice paper. Please try again.');
        this.generating = false;
      }
    });
  }

  // ── Paper actions ──────────────────────────────────────────────────────
  attemptOnline(paperId: string): void {
    this.router.navigate(['/practice-submit', paperId]);
  }

  attemptOffline(paperId: string): void {
    const studentName = this.auth.getCurrentUser()?.name || '';
    const url = `${this.apiBase}/practice/${paperId}/question-pdf?student_name=${encodeURIComponent(studentName)}`;
    this.http.get(url, { responseType: 'blob' }).subscribe({
      next: (blob) => {
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `practice_${paperId}.pdf`;
        a.click();
        URL.revokeObjectURL(a.href);
      },
      error: () => alert('Failed to download paper. Please try again.')
    });
  }

  uploadAnswers(paperId: string): void {
    this.router.navigate(['/practice-submit', paperId], { queryParams: { mode: 'upload' } });
  }

  // ── Load history ───────────────────────────────────────────────────────
  loadGeneratedPapers(): void {
    const userId = this.auth.getUserId();
    this.http.get<any[]>(`${this.apiBase}/practice/history/${userId}`).subscribe({
      next: (papers) => {
        this.generatedPapers = papers.map(p => ({
          paper_id: p.paper_id,
          subject_id: p.subject_id,
          topic_id: p.module_id,
          topic_name: p.module_id.replace(/-/g, ' ').replace(/\b\w/g, (l: string) => l.toUpperCase()),
          num_questions: p.num_questions,
          difficulty: p.difficulty.charAt(0).toUpperCase() + p.difficulty.slice(1),
          created_at: p.created_at,
          status: p.status || 'Not Attempted',
          score: p.score,
          percentage: p.percentage,
        }));
      },
      error: (err) => {
        console.error('Failed to load generated papers:', err);
      }
    });
  }

  getSubjectIcon(subjectId: string): string {
    return this.subjects.find(s => s.id === subjectId)?.icon
      || this.featuredSubjects.find(s => s.id === subjectId)?.icon
      || '📄';
  }

  formatDate(dateStr: string): string {
    return new Date(dateStr).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  }

  backToForm(): void {
    this.state = 'form';
    this.readyPaperId = '';
    this.readyPaperName = '';
  }

  goBack(): void {
    this.router.navigate(['/']);
  }
}
