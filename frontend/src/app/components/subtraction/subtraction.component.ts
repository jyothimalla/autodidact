import { Component, OnInit, HostListener } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { QuizService } from '../../services/quiz.service';
import { RightSidebarComponent } from '../right-sidebar/right-sidebar.component';
import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';
import { FooterComponent } from '../footer/footer.component';
import player from 'lottie-web';
import { AnimationOptions } from 'ngx-lottie';
import { AnimationItem } from 'lottie-web';

@Component({
  selector: 'app-subtraction',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RightSidebarComponent,
    LeftSidebarComponent,
    
  ],
  templateUrl: './subtraction.component.html',
  styleUrls: ['./subtraction.component.scss']
})


export class SubtractionComponent implements OnInit {
  questions: any[] = [];
  currentQIndex = 0;
  answerInput = '';
  feedbackMessage = '';
  score = 0;
  quizCompleted = false;
  level = 0;
  currentOperation = 'subtraction';
  userAnswers: string[] = [];
  username = '';
  user_id: number = 0;
  elapsedTime = '0:00'; 
  private timer: any;
  private secondsElapsed = 0;
  animation!: AnimationItem;

  lastUserAnswer = '';
  lastCorrectAnswer = '';
  isCorrect = true;

  constructor(private quizService: QuizService, private router: Router, private route:ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.username = params['username'] || localStorage.getItem('username') || '';
      this.user_id = parseInt(params['user_id'] || localStorage.getItem('user_id') || '0', 10);
      this.level = parseInt(params['level'] || '0', 10);
      this.currentOperation = params['operation'] || 'subtraction';
      this.currentQIndex = 0;
      console.log('📡 Fetching questions for level:', this.level);
  
      this.quizService.getSubtractionQuestions(this.level).subscribe({
        next: (questions) => {
          this.questions = questions;
  
          console.log('✅ Questions received:', questions);
  
          this.userAnswers = new Array(questions.length).fill('');
          this.startTimer();
        },
        error: (err) => console.error('❌ Error loading addition questions:', err)
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
    const user = this.answerInput.trim();
    if (!user) {
      alert('⚠️ Please enter your answer before submitting!');
      return;
    }
    this.lastUserAnswer = user;
    this.lastCorrectAnswer = correct;
    this.isCorrect = user === correct;

    if (this.isCorrect) {
      this.feedbackMessage = '✅ Correct!';
      this.score++;
    } else {
      this.feedbackMessage = `❌ Incorrect!`;
    }

    this.userAnswers[this.currentQIndex] = user;
    this.answerInput = '';

    setTimeout(() => {
      this.feedbackMessage = '';
    }, 1500);

    if (this.currentQIndex < this.questions.length - 1) {
      this.currentQIndex++;
    } else {
      this.completeQuiz();
    }
  }

  completeQuiz(): void {
    this.quizCompleted = true;

    localStorage.setItem('score', this.score.toString());
    localStorage.setItem('answers', JSON.stringify(this.userAnswers));
    localStorage.setItem('questions', JSON.stringify(this.questions));

    const progressKey = `${this.currentOperation}_progress`;
    const unlockedLevel = parseInt(localStorage.getItem(progressKey) || '0', 10);
    if (this.score === this.questions.length && this.level >= unlockedLevel) {
      localStorage.setItem(progressKey, (this.level + 1).toString());
    }

    setTimeout(() => this.router.navigate(['/result']), 1000);
  }

  restartQuiz(): void {
    this.router.navigate(['/operation']);
  }
  
  // Lottie Animation

handleLottie(anim: AnimationItem) {
  this.animation = anim;
}
isReading = false;

readQuestionAloud(): void {
  const question = this.questions[this.currentQIndex]?.question;
  if (question && 'speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(question);
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);

    this.animation?.play(); // Play animation
    utterance.onend = () => this.animation?.stop(); // Stop after speaking
  }
}
  
}
