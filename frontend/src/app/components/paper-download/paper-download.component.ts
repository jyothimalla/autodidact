import { Component, OnInit, Input, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { QuizService } from '../../services/quiz.service';
import { ConfigService } from '../../services/config.service';
import { Subscription } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-paper-download',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './paper-download.component.html',
  styleUrls: ['./paper-download.component.scss']
})
export class PaperDownloadComponent implements OnInit, OnDestroy {

  @Input() user_id: number = 0;
  @Input() username: string = '';
  @Input() operation: string = 'fmc';
  @Input() level: number = 0;

  sublevel: string = 'C';
  baseUrl: string = '';
  showAnswers: boolean = false;
  questions: any[] = [];

  private routeSub!: Subscription;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private quizService: QuizService,
    private config: ConfigService
  ) {}

  ngOnInit(): void {
    this.routeSub = this.route.queryParams.subscribe(params => {
      this.user_id = +params['user_id'] || this.user_id;
      this.username = params['username'] || this.username;
      this.operation = params['operation'] || this.operation;
      this.level = +params['level'] || this.level;
      this.sublevel = params['sublevel'] || 'this.sublevel';
      this.baseUrl = this.config.apiBaseUrl;
      if (this.sublevel === '0') {
      this.sublevel = 'C';
}
      console.log("📄 Generating paper for:", this.operation, this.level, this.username, this.user_id);
      console.log("Sublevel:", this.sublevel);
      this.fetchPaper();
    });
  }

  ngOnDestroy(): void {
    this.routeSub?.unsubscribe();
  }

  toggleAnswers(): void {
    this.showAnswers = !this.showAnswers;
  }

  fetchPaper(): void {
  const correctedSublevel = this.sublevel === '0' ? 'C' : this.sublevel;

  this.quizService.getPaper(this.user_id, this.level, correctedSublevel).subscribe({
    next: (data: any[]) => {
      this.questions = data;
    },
    error: err => console.error('❌ Failed to load paper', err)
  });
}


 downloadPaper(showAnswers: boolean): void {
  const url = `${this.baseUrl}/paper/fmc/generate-paper-pdf?user_id=${this.user_id}&level=${this.level}&show_answers=${showAnswers}`;

  this.http.get(url, { responseType: 'blob' }).subscribe({
    next: (blob: Blob) => {
      const fileURL = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = fileURL;
      a.download = showAnswers ? 'teacher_copy.pdf' : 'student_paper.pdf';
      a.click();
      URL.revokeObjectURL(fileURL);
    },
    error: err => console.error('❌ Download failed', err)
  });

  }
}
