import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-correct-paper',
  templateUrl: './correct-paper.component.html',
  styleUrls: ['./correct-paper.component.scss'],
  standalone: true,
  imports: [FormsModule, CommonModule],
})
export class CorrectPaperComponent {
  paperId = '';
  questions: any[] = [];
  results: any;

  constructor(private http: HttpClient) {}

  // Load paper questions from backend
  ngOnInit() {}

  submitAnswers() {
    const payload = {
      paper_id: this.paperId,
      answers: this.questions.map(q => ({
        question_id: q.question_id,
        student_answer: q.student_answer || '',
      })),
    };

    this.http.post<any>('http://localhost:8000/fmc/evaluate-paper', payload).subscribe(res => {
      this.results = res;
    });
  }

  // Load questions from DB if needed (or pass via route)
  loadQuestionsForPaper(paperId: string) {
    // Optional: Create a GET /fmc/paper/{paper_id} route if you want auto-load
  }
}
