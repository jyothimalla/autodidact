
import { Component, OnInit, HostListener } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { QuizService } from '../../services/quiz.service';
import { RightSidebarComponent } from '../right-sidebar/right-sidebar.component';
import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';
import confetti from 'canvas-confetti';

interface SubmitChallengeResponse {
  message: string;
  level_attempt_id: number;
  attempt_number: number;
  is_passed: boolean;
}

@Component({
  selector: 'app-multiplication',
  imports: [CommonModule, FormsModule, RightSidebarComponent, LeftSidebarComponent],
  standalone: true,
  templateUrl: './multiplication.component.html',
  styleUrl: './multiplication.component.scss'
})
export class MultiplicationComponent implements OnInit {
  questions: any[] = [];
  currentQIndex = 0;
  answerInput = '';
  feedbackMessage = '';
  score = 0;
  quizCompleted = false;
  level = 0;
  currentOperation = 'multiplication';
  userAnswers: string[] = [];
  username = '';
  user_id: number = 0;
  elapsedTime = '0:00';
  private timer: any;
  private secondsElapsed = 0;
  lastUserAnswer = '';
  lastCorrectAnswer = '';
  isCorrect = true;
  isReading = false;
  savingInProgress = false;
  explanation = '';
  showSpinner = false;
  showAnswer = false;
  showAnswerText = '';


  constructor(private quizService: QuizService, private router: Router, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.username = params['username'] || localStorage.getItem('username') || '';
      this.user_id = parseInt(params['user_id'] || localStorage.getItem('user_id') || '0', 10);
      this.level = parseInt(params['level'] || '0', 10);
      this.currentOperation = params['operation'] || 'multiplication';
      this.currentQIndex = 0;
      console.log('📡 Fetching questions for level:', this.level);
  
      this.quizService.getMultiplicationQuestions(this.level).subscribe({
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
    const userAnswer = this.answerInput.trim();
  
    if (!userAnswer) {
      alert('⚠️ Please enter your answer before submitting!');
      return;
    }
  
    this.lastUserAnswer = userAnswer;
    this.lastCorrectAnswer = correct;
    this.isCorrect = userAnswer === correct;
  
    this.feedbackMessage = this.isCorrect
      ? '✅ Correct!'
      : `❌ Incorrect! Correct is "${correct}"`;
  
    if (this.isCorrect) {
      this.score++;
    }
  
    this.userAnswers[this.currentQIndex] = userAnswer;
    this.answerInput = '';
  
    // ✅ Move to next question after very short delay
    
      if (this.currentQIndex < this.questions.length - 1) {
        this.currentQIndex++;   // move to next
      } else {
        this.completeQuiz();    // quiz complete
      }
      setTimeout(() => {
        this.feedbackMessage = ''; // clear message
    
    }, 800); // Just 0.8 seconds delay to show feedback
  }
  
  

  completeQuiz(): void {
    this.quizCompleted = true;
    this.savingInProgress = true; // Show spinner
  
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
      next: (response: SubmitChallengeResponse) => {
        
        console.log('Level Attempt ID:', response.level_attempt_id);
        console.log('Attempt Number:', response.attempt_number);
        console.log('Is Passed:', response.is_passed);
        const attemptNumber = response.attempt_number; // ✅ Pick attempt_number

        // 🎉 Play Confetti and Claps first
        if (this.score === this.questions.length) {
          this.launchConfetti();
          this.playClapSound();
        }
  
        setTimeout(() => {
          this.savingInProgress = false;
          this.router.navigate(['/result'], {
            queryParams: {
              username: this.username,
              user_id: this.user_id,
              operation: this.currentOperation,
              level: this.level,
              attempt_number: attemptNumber 
            }
          });
        }, 2500); 
      },
      error: (error) => {
        console.error('❌ Error saving attempt:', error);
        this.savingInProgress = false;
      }
    });
  }
  
  
  launchConfetti() {
    const duration = 3 * 1000; // 3 seconds
    const animationEnd = Date.now() + duration;
    const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 9999 };
  
    const interval: any = setInterval(function() {
      const timeLeft = animationEnd - Date.now();
  
      if (timeLeft <= 0) {
        return clearInterval(interval);
      }
  
      const particleCount = 50 * (timeLeft / duration);
  
      confetti(Object.assign({}, defaults, { particleCount, origin: { x: Math.random(), y: Math.random() - 0.2 } }));
    }, 250);
  }

  playClapSound() {
    const audio = new Audio();
    audio.src = 'assets/sounds/clap.mp3';  // Make sure you have a clap.mp3 inside assets/sounds
    audio.load();
    audio.play();
  }
  restartQuiz(): void {
    this.router.navigate(['/operation']);
  }

  readQuestionAloud(): void {
    const question = this.questions[this.currentQIndex]?.question;
    if (question && 'speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(question);
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utterance);
    }
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
