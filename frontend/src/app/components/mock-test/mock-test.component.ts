import { Component, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../../auth/auth.service';
import { environment } from '../../../environments/environment';

interface McqQuestion {
  question_number: number;
  question_id: string;
  module_id: string;
  question: string;
  options: { A: string; B: string; C: string; D: string };
}

interface ExamResult {
  score: number;
  total: number;
  percentage: number;
  passed: boolean;
  time_taken: number;
  breakdown: { label: string; score: number; total: number }[];
  review: {
    question_number: number;
    question: string;
    options: { A: string; B: string; C: string; D: string };
    your_answer: string;
    correct_option: string;
    correct_answer: string;
    explanation: string;
    is_correct: boolean;
  }[];
}

@Component({
  selector: 'app-mock-test',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './mock-test.component.html',
  styleUrls: ['./mock-test.component.scss'],
})
export class MockTestComponent implements OnDestroy {
  state: 'welcome' | 'loading' | 'exam' | 'submitted' = 'welcome';

  testId = '';
  questions: McqQuestion[] = [];
  answers: Record<string, string> = {};   // { q1: 'A', q2: 'C', ... }
  currentIndex = 0;
  errorMessage = '';
  showReview = false;
  result: ExamResult | null = null;

  // Timer
  timeLeft = 3600;   // seconds
  private timerHandle: ReturnType<typeof setInterval> | null = null;

  private readonly apiBase = environment.apiBaseUrl;

  readonly optionLabels: ('A' | 'B' | 'C' | 'D')[] = ['A', 'B', 'C', 'D'];

  constructor(
    private http: HttpClient,
    private auth: AuthService,
    private router: Router,
  ) {}

  get userId(): number {
    return this.auth.getUserId() ?? 0;
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

  questionStatus(q: McqQuestion): 'answered' | 'current' | 'unanswered' {
    if (q.question_number - 1 === this.currentIndex) return 'current';
    return this.answers[q.question_id] ? 'answered' : 'unanswered';
  }

  // ── Exam lifecycle ─────────────────────────────────────────────────────

  startExam(): void {
    this.errorMessage = '';
    this.state = 'loading';

    this.http.post<any>(`${this.apiBase}/test/generate`, {
      user_id: this.userId,
      difficulty: 'mixed',
    }).subscribe({
      next: (res) => {
        this.testId = res.test_id;
        this.questions = res.questions;
        this.timeLeft = res.time_limit_seconds ?? 3600;
        this.state = 'exam';
        this.startTimer();
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
        this.result = res;
        this.state = 'submitted';
      },
      error: () => {
        this.errorMessage = 'Failed to submit. Please try again.';
        this.startTimer();   // resume timer on failure
      },
    });
  }

  restartExam(): void {
    this.stopTimer();
    this.testId = '';
    this.questions = [];
    this.answers = {};
    this.currentIndex = 0;
    this.result = null;
    this.showReview = false;
    this.timeLeft = 3600;
    this.state = 'welcome';
  }

  ngOnDestroy(): void {
    this.stopTimer();
  }
}
