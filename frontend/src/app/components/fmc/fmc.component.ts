import { Component, OnInit } from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';
import { RightSidebarComponent } from '../right-sidebar/right-sidebar.component';
import { FooterComponent } from '../footer/footer.component';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-fmc',
  templateUrl: './fmc.component.html',
  styleUrls: ['./fmc.component.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule, LeftSidebarComponent, RightSidebarComponent, FooterComponent],
  providers: [QuizService]
})
export class FMCComponent implements OnInit {
  questions: any[] = [];
  currentQIndex = 0;
  userAnswer = '';
  feedbackMessage = '';
  score = 0;
  level = 0;
  userName = '';
  elapsedTime = '0:00';
  timer: any;
  secondsElapsed = 0;
  isFinished = false;

  constructor(private quizService: QuizService, private router: Router) {}

  ngOnInit(): void {
    this.level = parseInt(localStorage.getItem('level') || '0', 10);
    this.userName = localStorage.getItem('userName') || 'Guest';
    localStorage.setItem('operation', 'fmc');

    this.quizService.getFMCQuestions(this.level).subscribe({
      next: (res) => {
        this.questions = res;
        this.startTimer();
      },
      error: (err) => console.error('FMC fetch error:', err)
    });
  }

  submitAnswer(): void {
    const correct = this.questions[this.currentQIndex]?.answer;
    const user = this.userAnswer.trim();
    if (!user) {
    alert('⚠️ Please enter your answer before submitting!');
    return;
  }
    if (user === correct) {
      this.score++;
      this.feedbackMessage = '✅ Correct!';
    } else {
      this.feedbackMessage = `❌ Incorrect! Correct answer: ${correct}`;
    }
  
    this.userAnswer = ''; // clears input for the next question
  
    setTimeout(() => {
      this.feedbackMessage = '';
      if (this.currentQIndex < this.questions.length - 1) {
        this.currentQIndex++;
      } else {
        this.finishQuiz();
      }
    }, 1500);
  }

  startTimer(): void {
    this.timer = setInterval(() => {
      this.secondsElapsed++;
      const mins = Math.floor(this.secondsElapsed / 60);
      const secs = this.secondsElapsed % 60;
      this.elapsedTime = `${mins}:${secs < 10 ? '0' + secs : secs}`;
    }, 1000);
  }

  finishQuiz(): void {
    clearInterval(this.timer);
    this.isFinished = true;
    localStorage.setItem('score', this.score.toString());
  }

  tryAgain(): void {
    this.router.navigate(['/operation']);
  }
}
