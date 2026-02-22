import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../auth/auth.service';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-practice-submit',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './practice-submit.component.html',
  styleUrls: ['./practice-submit.component.scss']
})
export class PracticeSubmitComponent implements OnInit {
  attemptId: string = '';
  submissionType: 'upload' | 'manual' = 'manual';
  uploadFile: File | null = null;
  manualAnswers: Record<string, string> = {};
  numQuestions: number = 0;
  questions: any[] = [];
  submitting = false;
  result: any = null;
  private readonly apiBase = environment.apiBaseUrl;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient,
    private auth: AuthService
  ) {}

  ngOnInit(): void {
    this.attemptId = this.route.snapshot.paramMap.get('attemptId') || '';
    if (!this.attemptId) {
      alert('Invalid attempt ID');
      this.router.navigate(['/practice']);
      return;
    }

    const mode = this.route.snapshot.queryParamMap.get('mode');
    if (mode === 'upload') this.submissionType = 'upload';

    this.loadAttemptDetails();
  }

  loadAttemptDetails(): void {
    this.http.get<any>(`${this.apiBase}/practice/${this.attemptId}/details`).subscribe({
      next: (data) => {
        this.numQuestions = data.num_questions;
        this.questions = data.questions || [];
        for (let i = 1; i <= this.numQuestions; i++) {
          this.manualAnswers[`q${i}`] = '';
        }
      },
      error: (err) => {
        console.error('Failed to load attempt details:', err);
        alert('Failed to load practice attempt. Please try again.');
      }
    });
  }

  getOptionKeys(question: any): string[] {
    return question?.options ? Object.keys(question.options) : ['A', 'B', 'C', 'D'];
  }

  answeredCount(): number {
    return Object.values(this.manualAnswers).filter(a => a !== '').length;
  }

  onFileSelected(event: any): void {
    const files = event.target.files;
    if (files && files.length > 0) {
      this.uploadFile = files[0];
    }
  }

  submitViaUpload(): void {
    if (!this.uploadFile) {
      alert('Please select a file to upload');
      return;
    }
    this.submitting = true;
    const formData = new FormData();
    formData.append('file', this.uploadFile);
    this.http.post<any>(`${this.apiBase}/practice/${this.attemptId}/submit-upload`, formData).subscribe({
      next: (response) => {
        this.result = response;
        this.submitting = false;
      },
      error: (err) => {
        console.error('Upload failed:', err);
        alert('Failed to process upload. Please try entering answers manually.');
        this.submitting = false;
      }
    });
  }

  submitManually(): void {
    const filledAnswers = this.answeredCount();
    if (filledAnswers === 0) {
      alert('Please answer at least one question');
      return;
    }
    this.submitting = true;
    this.http.post<any>(`${this.apiBase}/practice/${this.attemptId}/submit`, {
      answers: this.manualAnswers
    }).subscribe({
      next: (response) => {
        this.result = response;
        this.submitting = false;
      },
      error: (err) => {
        console.error('Submission failed:', err);
        alert('Failed to submit answers. Please try again.');
        this.submitting = false;
      }
    });
  }

  getQuestionNumbers(): number[] {
    return Array.from({ length: this.numQuestions }, (_, i) => i + 1);
  }

  goBack(): void {
    this.router.navigate(['/practice']);
  }
}
