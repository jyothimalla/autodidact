// src/app/components/division/division.component.ts
import { Component, OnInit, HostListener, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { QuizService } from '../../services/quiz.service';
import { RightSidebarComponent } from '../right-sidebar/right-sidebar.component';
import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';
import confetti from 'canvas-confetti';
import { AnimationItem } from 'lottie-web';

interface SubmitChallengeResponse {
  message: string;
  level_attempt_id: number;
  attempt_number: number;
  is_passed: boolean;
}

@Component({
  selector: 'app-division',
  standalone: true,
  imports: [CommonModule, FormsModule, RightSidebarComponent, LeftSidebarComponent],
  templateUrl: './division.component.html',
  styleUrl: './division.component.scss'
})
export class DivisionComponent implements OnInit, OnDestroy {
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
  savingInProgress = false;
  animation: AnimationItem | undefined;
  isReading = false;
  explanation = '';
  showSpinner = false;
  
  constructor(private quizService: QuizService, private router: Router, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.username = params['username'] || localStorage.getItem('username') || '';
      this.user_id = parseInt(params['user_id'] || localStorage.getItem('user_id') || '0', 10);
      this.level = parseInt(params['level'] || '0', 10);
      this.currentOperation = params['operation'] || 'division';
      this.currentQIndex = 0;
       // ✅ Start session before loading questions
       this.startSession();
       // loading Questions
       console.log('📡 Fetching questions for level:', this.level);
       this.fetchQuestions();
      
    });
  }

  fetchQuestions(): void {

    this.quizService.getDivisionQuestions(this.level).subscribe({
      next: (questions) => {
        this.questions = questions;
        this.userAnswers = new Array(questions.length).fill('');
        localStorage.setItem('startTime', Date.now().toString());

        this.startTimer();
      },
      error: (err) => console.error('❌ Error loading division questions:', err)
    });
  }
  startSession(): void {
    if (!this.username || !this.user_id) {
      alert("⚠️ You must be logged in to start the quiz.");
      this.router.navigate(['/login']);
      return;
    }
    this.username = this.username.trim();
    this.quizService.startSession(this.username, this.currentOperation, this.level).subscribe({
      next: (res) => {
        console.log('✅ Session started:', res.session_id);
      },
      error: (err) => {
        console.error('❌ Failed to start session:', err);
      }
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
    if (this.quizCompleted) return;

    const currentQ = this.questions[this.currentQIndex];
    const correct = currentQ.answer.trim();
    const userAnswer = this.answerInput.trim();

    if (!userAnswer) {
      alert('⚠️ Please enter your answer!');
      return;
    }

    this.isCorrect = userAnswer === correct;
    this.feedbackMessage = this.isCorrect ? '✅ Correct!' : `❌ Incorrect! Correct answer: ${correct}`;

    if (this.isCorrect) this.score++;

    this.userAnswers[this.currentQIndex] = userAnswer;
    this.answerInput = '';

    if (this.currentQIndex < this.questions.length - 1) {
      this.currentQIndex++;
    } else {
      this.finishQuiz();
    }

    setTimeout(() => this.feedbackMessage = '', 800);
  }

  finishQuiz(): void {
    this.quizCompleted = true;
    clearInterval(this.timer);
    this.savingInProgress = true;

    localStorage.setItem('score', this.score.toString());
    localStorage.setItem('answers', JSON.stringify(this.userAnswers));
    localStorage.setItem('questions', JSON.stringify(this.questions));

    const progressKey = `${this.currentOperation}_progress`;
    const unlocked = parseInt(localStorage.getItem(progressKey) || '0', 10);
    if (this.score === this.questions.length && this.level >= unlocked) {
      localStorage.setItem(progressKey, (this.level + 1).toString());
      this.feedbackMessage = '🎉 Challenge Completed!';
      this.launchConfetti();
      this.playClapSound();
    }

    this.quizService.submitChallengeAttempt({
      user_id: this.user_id,
      operation: this.currentOperation,
      level: this.level,
      score: this.score,
      total_questions: this.questions.length
    }).subscribe({
      next: (response: SubmitChallengeResponse) => {
        console.log('✅ Attempt saved!', response);

        if (response.is_passed) {
          this.launchConfetti();
          this.playClapSound();
        }

        setTimeout(() => {
          this.savingInProgress = false;
          alert(`🎉 Congratulations ${this.username}! You completed Level ${this.level}!\n⭐ Promoted to Level ${this.level + 1}`);
          this.router.navigate(['/result'], {
            queryParams: {
              username: this.username,
              user_id: this.user_id,
              operation: this.currentOperation,
              level: this.level,
              attempt_number: response.attempt_number
            }
          });
        }, 2500);
      },
      error: (err) => {
        console.error('❌ Error saving attempt:', err);
        this.savingInProgress = false;
      }
    });
  }

  launchConfetti() {
    const duration = 3 * 1000;
    const animationEnd = Date.now() + duration;
    const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 9999 };

    const interval = setInterval(() => {
      const timeLeft = animationEnd - Date.now();
      if (timeLeft <= 0) return clearInterval(interval);

      const particleCount = 50 * (timeLeft / duration);
      confetti(Object.assign({}, defaults, { particleCount, origin: { x: Math.random(), y: Math.random() - 0.2 } }));
    }, 250);
  }

  playClapSound() {
    const audio = new Audio('assets/sounds/claps.mp3');
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

      this.animation?.play();
      utterance.onend = () => this.animation?.stop();
    }
  }
  ngOnDestroy(): void {
    if (this.timer) clearInterval(this.timer);
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
  goToLearn(): void {
    this.router.navigate([`/learn/${this.currentOperation}`], {
      queryParams: {
        level: this.level,
        username: this.username,
        user_id: this.user_id
      }
    });
  }
  printQuestions(): void {
    const printableContent = this.questions.map((q, index) => `
      <div style="margin-bottom: 20px;">
        <div><strong>Q${index + 1}:</strong> ${q.question}
        <div style="border: 1px solid #000; width: 40px; height: 30px; margin-top: 8px;"></div>
      </div></div>
    `).join('');
  
    const printWindow = window.open('', '', 'height=800,width=800');
  
    if (printWindow) {
      printWindow.document.write('<html><head><title>Quiz Questions</title></head><body>');
      printWindow.document.write('<h1 style="text-align:center;">Quiz Paper</h1>');
      printWindow.document.write(printableContent);
      printWindow.document.write('</body></html>');
      printWindow.document.close();
      printWindow.print();
    }
  }
  
}
