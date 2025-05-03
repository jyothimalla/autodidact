import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DomSanitizer } from '@angular/platform-browser';

import confetti from 'canvas-confetti';
import { AnimationItem } from 'lottie-web';

import { QuizService } from '../../services/quiz.service';
import { ExampleService } from '../../services/example.service';

import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';
import { RightSidebarComponent } from '../right-sidebar/right-sidebar.component';

@Component({
  selector: 'app-practice',
  standalone: true,
  imports: [CommonModule, FormsModule, LeftSidebarComponent, RightSidebarComponent],
  templateUrl: './practice.component.html',
  styleUrl: './practice.component.scss'
})
export class PracticeComponent implements OnInit, OnDestroy {
  questions: any[] = [];
  userAnswers: string[] = [];
  answerInput = '';
  feedbackMessage = '';
  explanation = '';
  score = 0;
  level = 0;
  quizCompleted = false;
  isCorrect = true;
  isReading = false;
  isEnterDisabled = false;
  savingInProgress = false;

  operation = 'addition';
  username = '';
  user_id = 0;
  currentQIndex = 0;
  elapsedTime = '0:00';
  private timer: any;
  private secondsElapsed = 0;
  mode: 'practice' | 'guest' = 'practice';

  animation!: AnimationItem;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private quizService: QuizService,
    private exampleService: ExampleService,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.level = parseInt(params['level'] || '0', 10);
      this.username = params['username'] || localStorage.getItem('username') || 'Guest';
      this.user_id = parseInt(localStorage.getItem('user_id') || '0', 10);
      this.operation = this.route.snapshot.params['operation'] || 'addition';

      this.mode = this.username === 'Guest' ? 'guest' : 'practice';

      if (this.mode === 'guest' && this.guestAlreadyPlayedToday()) {
        alert('🚫 Guests can only practice once per day.');
        return;
      }

      this.loadQuestions();
    });
  }

  guestAlreadyPlayedToday(): boolean {
    const today = new Date().toISOString().slice(0, 10);
    const lastPlayed = localStorage.getItem('guest_played_on');
    if (lastPlayed === today) return true;
    localStorage.setItem('guest_played_on', today);
    return false;
  }

  loadQuestions(): void {
    const mode: 'practice' | 'challenge' | 'guest' =
      this.username === 'Guest' ? 'guest' : 'practice';

    if (mode === 'guest') {
      const today = new Date().toISOString().slice(0, 10);
      const lastPlayed = localStorage.getItem('guest_played_on');

      if (lastPlayed === today) {
        alert('🚫 Guests can only practice once per day.');
        return;
      } else {
        localStorage.setItem('guest_played_on', today);
      }
    }

    this.quizService.getQuestionsByOperation(this.operation, this.level, this.mode).subscribe({
      next: questions => {
        this.questions = questions;
        this.userAnswers = new Array(questions.length).fill('');
        this.startTimer();
      },
      error: err => console.error('❌ Failed to load questions:', err)
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
    this.feedbackMessage = this.isCorrect ? '✅ Correct!' : `❌ Incorrect Answer! The Correct Answer is: ${correct}`;

    if (this.isCorrect) this.score++;
    this.userAnswers[this.currentQIndex] = userAnswer;
    this.answerInput = '';

    if (++this.currentQIndex < this.questions.length) return;

    this.quizCompleted = true;
    clearInterval(this.timer);
    this.feedbackMessage = '🎉 Practice Completed!';
    setTimeout(() => this.finishQuiz(), 1500);
  }

  finishQuiz(): void {
    console.log('🎯 Final Score:', this.score);
    this.savingInProgress = true;

    localStorage.setItem('score', this.score.toString());
    localStorage.setItem('answers', JSON.stringify(this.userAnswers));
    localStorage.setItem('questions', JSON.stringify(this.questions));

    const localKey = `practice_${this.operation}_level${this.level}`;
    const progressKey = `${this.operation}_progress`;
    const unlocked = parseInt(localStorage.getItem(progressKey) || '0', 10);
    if (this.score === this.questions.length && this.level >= unlocked) {
      localStorage.setItem(progressKey, (this.level + 1).toString());
    }
    

    localStorage.setItem(localKey, JSON.stringify({
      score: this.score,
      total: this.questions.length,
      date: new Date().toISOString()
    }));
    
    console.log(`📚 Practice result saved locally as ${localKey}`);

    
  }

  navigateToResult(): void {
    this.router.navigate(['/result'], {
      queryParams: {
        username: this.username,
        user_id: this.user_id,
        operation: this.operation,
        level: this.level
      }
    });
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

  goToNextLevel(): void {
    localStorage.setItem('level', (this.level + 1).toString());
    this.router.navigate([`/operation/${this.operation}/${this.level + 1}`]);
  }

  printQuestions(): void {
    const html = this.questions.map((q, i) => `
      <div style="margin-bottom: 20px;">
        <strong>Q${i + 1}:</strong> ${q.question}
        <div style="border: 1px solid #000; width: 40px; height: 30px; margin-top: 8px;"></div>
      </div>
    `).join('');

    const win = window.open('', '', 'height=800,width=800');
    if (win) {
      win.document.write('<html><head><title>Quiz Questions</title></head><body>');
      win.document.write('<h1 style="text-align:center;">Quiz Paper</h1>');
      win.document.write(html);
      win.document.write('</body></html>');
      win.document.close();
      win.print();
    }
  }

  playClapSound(): void {
    new Audio('assets/sounds/claps.mp3').play();
  }
  takeChallenge(): void {
    this.router.navigate([`/${this.operation}`], {
      queryParams: {
        level: this.level,
        username: this.username,
        user_id: this.user_id
      }
    });
  }
  goToLearn(): void {
    this.router.navigate([`/learn/${this.operation}`], {
      queryParams: {
        level: this.level,
        username: this.username,
        user_id: this.user_id
      }
    });
  }

  goHome(): void {
    clearInterval(this.timer);
    localStorage.clear();
    this.router.navigate(['/']);
  }

  restartQuiz(): void {
    this.router.navigate(['/operation']);
  }

  goBack(): void {
   
    this.router.navigate([`/${this.operation}`]);
  }

  ngOnDestroy(): void {
    if (this.timer) clearInterval(this.timer);
  }
}
