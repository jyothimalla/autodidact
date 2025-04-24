import { Component, OnInit } from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { ActivatedRoute, Router } from '@angular/router';
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
  username = '';
  user_id: number = 0;
  elapsedTime = '0:00';
  timer: any;
  secondsElapsed = 0;
  isFinished = false;
  currentOperation = 'fmc';
  isEnterDisabled = false;
  lastUserAnswer = '';
  lastCorrectAnswer = '';
  userAnswers: string[] = [];

  constructor(private quizService: QuizService, private router: Router, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.username = params['username'] || localStorage.getItem('username') || '';
      this.user_id = parseInt(params['user_id'] || localStorage.getItem('user_id') || '0', 10);
      this.level = parseInt(params['level'] || '0', 10);
      this.currentOperation = params['operation'] || 'fmc';
      this.currentQIndex = 0;
      console.log('📡 Fetching questions for level:', this.level);
  
      this.quizService.getFMCQuestions(this.level).subscribe({
        next: (questions) => {
          this.questions = questions;
  
          console.log('✅ Questions received:', questions);
  
          this.userAnswers = new Array(questions.length).fill('');
          this.startTimer();
        },
        error: (err) => console.error('❌ Error loading FMC questions:', err)
      });     
    });
  }
  submitAnswer(): void {
    const currentQ = this.questions[this.currentQIndex];
    const correct = currentQ?.answer.trim();
    const userAnswer = this.userAnswer.trim();
  
    if (!userAnswer) {
      alert('⚠️ Please enter your answer before submitting!');
      return;
    }
  
    if (userAnswer === correct) {
      this.score++;
      this.feedbackMessage = '✅ Correct!';
    } else {
      this.feedbackMessage = `❌ Incorrect! Correct answer: ${correct}`;
    }
  
    this.userAnswer = ''; // clear input
  
    setTimeout(() => {
      this.feedbackMessage = '';
      if (this.currentQIndex < this.questions.length - 1) {
        this.currentQIndex++;
      } else {
        this.completeQuiz();  // or finishQuiz(), whichever is your finalizer
      }
    }, 1000);  // optional: delay feedback
  }
  
  completeQuiz(): void {
    clearInterval(this.timer);
    this.isFinished = true;
    localStorage.setItem('score', this.score.toString());
    localStorage.setItem('answers', JSON.stringify(this.questions.map(q => q.answer)));
    localStorage.setItem('questions', JSON.stringify(this.questions));
    localStorage.setItem('explanation', JSON.stringify(this.questions.map(q => q.explanation)));
    
    const progressKey = `${this.currentOperation}_progress`;
    const unlockedLevel = parseInt(localStorage.getItem(progressKey) || '0', 10);

    if (this.score === this.questions.length && this.level >= unlockedLevel) {
      localStorage.setItem(progressKey, (this.level + 1).toString());
    }

    setTimeout(() => this.router.navigate(['/result']), 1000);
    
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
  reviewAnswers(): void {
    this.router.navigate(['/result'], { queryParams: { score: this.score, elapsedTime: this.elapsedTime } });
  }
}
