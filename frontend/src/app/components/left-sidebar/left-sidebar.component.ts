import { Component, OnInit } from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-left-sidebar',
  imports: [CommonModule, FormsModule],
  templateUrl: './left-sidebar.component.html',
  styleUrls: ['./left-sidebar.component.scss'],
  standalone: true,
})

export class LeftSidebarComponent implements OnInit {
  userName = '';
  questions: any[] = [];
  currentQIndex = 0;
  currentOperation = '';
  answerInput: string = '';
  score = 0;
  attemptedCount = 0;
  feedbackMessage = '';
  explanation = '';
  elapsedTime = '0:00';
  userAnswers: string[] = [];
  quizCompleted = false;
  level: number = 0;
  isSudoku: boolean = false;
  private timer: any;
  private secondsElapsed = 0;

  constructor(private quizService: QuizService, private router: Router) {}
  ngOnInit(): void {
    const storedName = localStorage.getItem('userName');
    const operation = localStorage.getItem('operation') || 'addition';
    const level = parseInt(localStorage.getItem('level') || '0', 10);
    
    if (operation === 'sudoku') {
      this.isSudoku = true;
      this.router.navigate(['/sudoku']);
      return; // no need to call quizService for questions
    }
    if (storedName) {
      this.userName = storedName;
      this.currentOperation = operation;
      this.quizService.getQuestions(this.userName).subscribe(data => {
        this.questions = data;
        this.startTimer();
      });
    } else {
      this.router.navigate(['/']);
    }
  }
  startTimer() {
    this.timer = setInterval(() => {
      this.secondsElapsed++;
      const minutes = Math.floor(this.secondsElapsed / 60);
      const seconds = this.secondsElapsed % 60;
      this.elapsedTime = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }, 1000);
  }

switchOperation(operation: string) {
  this.currentOperation = operation;
  localStorage.setItem('operation', operation);
  this.router.navigate(['/addition']);
  this.quizService.getQuestions(this.userName).subscribe(data => {
    this.questions = data;
    this.startTimer();
  }
  );
  this.router.navigate(['/addition']);
  this.quizService.getQuestions(this.userName).subscribe(data => {
    this.questions = data;
    this.startTimer();
  }
  );
  
}
goBack(): void {
  clearInterval(this.timer);
  this.router.navigate(['/']);
  localStorage.removeItem('userName');
  localStorage.removeItem('operation');
  localStorage.removeItem('level');
  localStorage.removeItem('score');
  this.router.navigate(['/operation']);
}
goHome(): void {
  clearInterval(this.timer);
  localStorage.removeItem('userName');
  localStorage.removeItem('operation');
  localStorage.removeItem('level');
  localStorage.removeItem('score');
  this.router.navigate(['/']);
}
}
