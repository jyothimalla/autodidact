import { Component, OnInit, HostListener } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { QuizService } from '../../services/quiz.service';
import { RightSidebarComponent } from '../right-sidebar/right-sidebar.component';
import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';
import { HeaderComponent } from '../header/header.component';
import player from 'lottie-web';
import { AnimationOptions, LottieComponent } from 'ngx-lottie';
import { AnimationItem } from 'lottie-web';
import { LottieServerModule } from 'ngx-lottie/server';
import { ActivatedRoute } from '@angular/router';

export function playerFactory() {
  return player;
}


@Component({
  selector: 'app-addition',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RightSidebarComponent,
    LeftSidebarComponent,],
  templateUrl: './addition.component.html',
  styleUrls: ['./addition.component.scss']
})


export class AdditionComponent implements OnInit {
  questions: any[] = [];
  currentQIndex = 0;
  answerInput = '';
  feedbackMessage = '';
  score = 0;
  quizCompleted = false;
  level = 0;
  currentOperation = 'addition';
  userAnswers: string[] = [];
  username: string = '';
  elapsedTime = '0:00'; 
  private timer: any;
  private secondsElapsed = 0;
  animation!: AnimationItem;
  isEnterDisabled = false;
  lastUserAnswer = '';
  lastCorrectAnswer = '';
  isCorrect = true;
  user_id: number = 0;
  explanation  = '';
  savingInProgress = false;

  constructor(private quizService: QuizService, private router: Router, private route: ActivatedRoute) {}

  

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
    this.username = params['username'] || localStorage.getItem('username') || '';
    this.user_id = parseInt(params['user_id'] || localStorage.getItem('user_id') || '0', 10);
    this.level = parseInt(params['level'] || '0', 10);
    this.currentOperation = params['operation'] || 'addition';
    this.currentQIndex = 0;
    console.log('📡 Fetching questions for level:', this.level);

    this.quizService.getAdditionQuestions(this.level).subscribe({
      next: (questions) => {
        this.questions = questions;

        console.log('✅ Questions received:', questions);

        this.userAnswers = new Array(questions.length).fill('');
        this.startTimer();
      },
      error: (err) => console.error('❌ Error loading addition questions:', err)
    }); });

    
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
  if (!this.isEnterDisabled) {
    this.isEnterDisabled = true;  // Prevent rapid fire
    this.submitAnswer();
    setTimeout(() => { this.isEnterDisabled = false;}, 1500); 
  }
}


  submitAnswer(): void {
    const currentQ = this.questions[this.currentQIndex];
    const correct = currentQ.answer.trim();
    const userAnswer = this.answerInput.trim();

    if (!userAnswer) {
      alert('⚠️ Please enter your answer before submitting!');
      return;
    }
    this.lastUserAnswer = userAnswer;
    this.lastCorrectAnswer = correct;
    this.isCorrect = userAnswer === correct;
    this.feedbackMessage = this.isCorrect ? '✅ Correct!' : `❌ Incorrect! The correct answer is ${correct}`;
    if (this.isCorrect) 
      this.score++;

    this.userAnswers[this.currentQIndex] = userAnswer;
    this.answerInput = '';
    
    setTimeout(() => {
      this.feedbackMessage = '';
      if (this.currentQIndex < this.questions.length - 1) {
        this.currentQIndex++;
      } else {
        this.completeQuiz();
      }
    }, 2500);
  }
  

  completeQuiz(): void {
    this.quizCompleted = true;
    this.savingInProgress = true; // 🔵 Start showing spinner
  
    localStorage.setItem('score', this.score.toString());
    localStorage.setItem('answers', JSON.stringify(this.userAnswers));
    localStorage.setItem('questions', JSON.stringify(this.questions));
  
    const progressKey = `${this.currentOperation}_progress`;
    const unlockedLevel = parseInt(localStorage.getItem(progressKey) || '0', 10);
    if (this.score === this.questions.length && this.level >= unlockedLevel) {
      localStorage.setItem(progressKey, (this.level + 1).toString());
    }
  
    this.quizService.submitChallengeAttempt({
      user_id: this.user_id,
      operation: this.currentOperation,
      level: this.level,
      score: this.score,
      total_questions: this.questions.length
    }).subscribe({
      next: (response) => {
        console.log('✅ Attempt saved successfully!', response);
  
        setTimeout(() => {
          this.savingInProgress = false; // 🟢 Stop spinner after small wait
          this.router.navigate(['/result'], {
            queryParams: {
              username: this.username,
              user_id: this.user_id,
              operation: this.currentOperation,
              level: this.level
            }
          });
        }, 1500); // ⏳ Wait 1.5 seconds to show spinner properly
      },
      error: (error) => {
        console.error('❌ Error saving attempt:', error);
        this.savingInProgress = false; // 🔴 Hide spinner on error too
      }
    });
  }
  

  restartQuiz(): void {
    this.router.navigate(['/operation']);
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
  
ngOnDestroy(): void {
  if (this.timer) clearInterval(this.timer);
}
goHome(): void {
  clearInterval(this.timer);
  localStorage.removeItem('userName');
  localStorage.removeItem('operation');
  localStorage.removeItem('level');
  localStorage.removeItem('score');
  this.router.navigate(['/']);
}

  goBack(): void {
    if (this.currentQIndex > 0) {
      this.currentQIndex--;
      this.answerInput = this.userAnswers[this.currentQIndex] || '';
    }
    this.feedbackMessage = '';
    this.explanation = '';
    this.router.navigate(['/operation']);
  }
}
