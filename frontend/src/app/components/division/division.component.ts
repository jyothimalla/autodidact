// src/app/components/division/division.component.ts
import { Component, OnInit, HostListener } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { QuizService } from '../../services/quiz.service';
import { RightSidebarComponent } from '../right-sidebar/right-sidebar.component';
import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';
import { FooterComponent } from '../footer/footer.component';

@Component({
  selector: 'app-division',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RightSidebarComponent,
    LeftSidebarComponent,
    FooterComponent,
  ],
  templateUrl: './division.component.html',
  styleUrls: ['./division.component.scss']
})
export class DivisionComponent implements OnInit {
  questions: any[] = [];
  currentQIndex = 0;
  answerInput = '';
  feedbackMessage = '';
  score = 0;
  quizCompleted = false;
  level = 0;
  username = '';
  user_id: number = 0;
  currentOperation = 'division';
  userAnswers: string[] = [];
  elapsedTime = '0:00';
  private timer: any;
  private secondsElapsed = 0;
  isCorrect = true;
  lastCorrectAnswer = '';

  constructor(private quizService: QuizService, private router: Router, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.username = params['username'] || localStorage.getItem('username') || '';
      this.user_id = parseInt(params['user_id'] || localStorage.getItem('user_id') || '0', 10);
      this.level = parseInt(params['level'] || '0', 10);
      this.currentOperation = params['operation'] || 'division';
      this.currentQIndex = 0;
      console.log('📡 Fetching questions for level:', this.level);
  
      this.quizService.getDivisionQuestions(this.level).subscribe({
        next: (questions) => {
          this.questions = questions;
  
          console.log('✅ Questions received:', questions);
  
          this.userAnswers = new Array(questions.length).fill('');
          this.startTimer();
        },
        error: (err) => console.error('❌ Error loading Division questions:', err)
      });     
    });
  }
  startTimer(): void {
    this.timer = setInterval(() => {
      this.secondsElapsed++;
      const minutes = Math.floor(this.secondsElapsed / 60);
      const seconds = this.secondsElapsed % 60;
      this.elapsedTime = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }, 1000);
  }

  @HostListener('document:keydown.enter', ['$event'])
  handleEnter(event: KeyboardEvent) {
    this.submitAnswer();
  }

  submitAnswer(): void {
    const currentQ = this.questions[this.currentQIndex];
    const correct = currentQ.answer.trim();
    const userAnswer = this.answerInput.trim();

    if (!userAnswer) {
      alert('⚠️ Please enter your answer before submitting!');
      return;
    }
    this.isCorrect = userAnswer === correct;
    this.lastCorrectAnswer = correct;
    this.feedbackMessage = this.isCorrect ? '✅ Correct!' : `❌ Incorrect! Correct is ${correct}`;
    if (this.isCorrect) this.score++;

    this.userAnswers[this.currentQIndex] = userAnswer;
    this.answerInput = '';

    setTimeout(() => this.feedbackMessage = '', 1500);

    if (this.currentQIndex < this.questions.length - 1) {
      this.currentQIndex++;
    } else {
      this.finishQuiz();
    }
  }

  finishQuiz(): void {
    this.quizCompleted = true;
    localStorage.setItem('score', this.score.toString());
    localStorage.setItem('answers', JSON.stringify(this.userAnswers));
    localStorage.setItem('questions', JSON.stringify(this.questions));

    const progressKey = `${this.currentOperation}_progress`;
    const unlocked = parseInt(localStorage.getItem(progressKey) || '0', 10);
    if (this.score === this.questions.length && this.level >= unlocked) {
      localStorage.setItem(progressKey, (this.level + 1).toString());
    }

    setTimeout(() => this.router.navigate(['/result']), 1000);
  }

  restartQuiz(): void {
    this.router.navigate(['/operation']);
  }
}
