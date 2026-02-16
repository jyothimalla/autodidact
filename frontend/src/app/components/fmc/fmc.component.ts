import { Component, OnInit } from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';
import { RightSidebarComponent } from '../right-sidebar/right-sidebar.component';
import { FormsModule } from '@angular/forms';
import { PaperDownloadComponent } from "../paper-download/paper-download.component";

@Component({
  selector: 'app-fmc',
  templateUrl: './fmc.component.html',
  styleUrls: ['./fmc.component.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule, LeftSidebarComponent, RightSidebarComponent, PaperDownloadComponent],
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
  isAnimationPlaying = false;
  explanation = '';
  animation: any;
  answerInput = '';
  isCorrect = true;
  quizCompleted = false;
  operation = 'fmc';

  constructor(private quizService: QuizService, private router: Router, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.username = params['username'] || localStorage.getItem('username') || '';
      this.user_id = parseInt(params['user_id'] || localStorage.getItem('user_id') || '0', 10);
      this.level = parseInt(params['level'] || '0', 10);
      this.operation = params['operation'] || 'fmc';
      this.currentQIndex = 0;
      // ✅ Start session before loading questions
      this.startSession();
      
      console.log('📡 Fetching questions for level:', this.level);
      this.fetchQuestions();
    });
  }
  startSession(): void {
    if (!this.username || !this.user_id) {
      alert("⚠️ You must be logged in to start the quiz.");
      this.router.navigate(['/login']);
      return;
    }
    this.username = this.username.trim();
    this.quizService.startSession(this.username, this.operation, this.level).subscribe({
      next: (res) => {
        console.log('✅ Session started:', res.session_id);
      },
      error: (err) => {
        console.error('❌ Failed to start session:', err);
      }
    });
  }
  fetchQuestions(): void {
    this.quizService.getFMCQuestions(this.level).subscribe({
      next: (questions) => {
        this.questions = questions;

        console.log('✅ Questions received:', questions);

        this.userAnswers = new Array(questions.length).fill('');
        localStorage.setItem('startTime', Date.now().toString());

        this.startTimer();
      },
      error: (err) => console.error('❌ Error loading FMC questions:', err)
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
    this.quizCompleted = true;
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
  restartQuiz(): void {
    this.router.navigate(['/operation']);
  }

  tryAgain(): void {
    this.router.navigate(['/operation']);
  }
  reviewAnswers(): void {
    this.router.navigate(['/result'], { queryParams: { score: this.score, elapsedTime: this.elapsedTime } });
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
  takeChallenge(): void {
    this.router.navigate([`/${this.currentOperation}`], {
      queryParams: {
        level: this.level,
        username: this.username,
        user_id: this.user_id
      }
    });
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
