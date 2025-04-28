import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { Router } from '@angular/router';
import { PLATFORM_ID } from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { FooterComponent } from "../footer/footer.component";
import { ActivatedRoute } from '@angular/router';
import confetti from 'canvas-confetti';


@Component({
  selector: 'app-result',
  standalone: true,
  imports: [CommonModule, FooterComponent],
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss']
})
export class ResultComponent implements OnInit {
  platformId = inject(PLATFORM_ID);

  username: string = '';
  score: number = 0;
  total: number = 0;
  userAnswers: string[] = [];
  questions: any[] = [];
  explanation: string = '';
  operation: string = '';
  level: number = 0;
  user_id: number = 0;
  levelUnlocked: boolean = false;
  performanceStar: string = '';
  performanceTitle: string = '';
  performanceMessage: string = '';
  performanceEmoji: string = '';
  performanceColor: string = '';
  attemptNumber: number = 1;

  
  get attemptedCount(): number {
    return this.userAnswers.filter(ans => ans && ans.trim() !== '').length;
  }

  constructor(private router: Router, private quizService: QuizService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.username = this.route.snapshot.queryParams['username'] || localStorage.getItem('username') || '';
    this.user_id = parseInt(localStorage.getItem('user_id') || '0', 10);
    console.log('Storing user_id:', this.user_id, 'username:', this.username);
    console.log('🧠 Username:', this.username);
    
    const storedScore = localStorage.getItem('score');
    const storedAnswers = localStorage.getItem('answers');
    const storedQuestions = localStorage.getItem('questions');
    const storedExplanation = localStorage.getItem('explanation');
    const operation = localStorage.getItem('operation') || 'addition';
    const level = parseInt(localStorage.getItem('level') || '0', 10);
    this.attemptNumber = parseInt(this.route.snapshot.queryParams['attempt_number'] || '1', 10);

    this.operation = operation;
    this.level = level;
    if (!this.username || !storedScore || !storedAnswers || !storedQuestions) {
    this.router.navigate(['/']);
    return;
    }
    try {
    this.username = this.username;
    this.score = parseInt(storedScore);
    this.userAnswers = JSON.parse(storedAnswers);
    this.questions = JSON.parse(storedQuestions);
    this.total = this.questions.length;
    }catch (err){
      console.error("❌ Failed to parse stored data:", err);
      this.router.navigate(['/']);
    }

    this.operation = localStorage.getItem('operation') || 'addition';
    this.level = parseInt(localStorage.getItem('level') || '0', 10);

    this.questions.forEach((q, i) => {
      if (!q.correctValue && q.answer) {
        q.correctValue = q.answer; // fallback
      }
    });

  
    // ✅ Check and unlock progress only if needed
    if (this.score === 10) {
      const progressKey = `${this.operation}_progress`;
      const currentUnlocked = parseInt(localStorage.getItem(progressKey) || '0', 10);

      console.log('🚀 Current unlocked level:', currentUnlocked);
      console.log('🧠 This level attempted:', this.level);

      if (this.level === currentUnlocked) {
        localStorage.setItem(progressKey, (currentUnlocked + 1).toString());
        this.levelUnlocked = true; 
        if (this.levelUnlocked) {
          this.launchConfetti();
        }
        console.log('✅ New level unlocked:', currentUnlocked + 1);
      } else {
        console.log('ℹ️ No new level unlocked (already unlocked before).');
      }
}

  }
  launchConfetti() {
    const duration = 5 * 1000; // 5 seconds
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
  
  calculatePerformanceStar(): void {
    if (this.attemptNumber === 1) {
      this.performanceStar = '🥇';
      this.performanceTitle = 'Perfect Champion';
    } else if (this.attemptNumber === 2) {
      this.performanceStar = '🥈';
      this.performanceTitle = 'Great Fighter';
    } else {
      this.performanceStar = '🥉';
      this.performanceTitle = 'Persistent Learner';
    }
  }

  goHome(): void {
    localStorage.removeItem('score');
    localStorage.removeItem('answers');
    localStorage.removeItem('questions');
    localStorage.removeItem('operation');
    this.router.navigate(['/']);
  }
  nextLevel(): void {
    const nextLevel = this.level + 1;
    const currentOperation = localStorage.getItem('operation'); // or pass it in as input
    localStorage.setItem('level', nextLevel.toString());
    this.router.navigate([`/operation/${currentOperation}/${nextLevel}`]);
  }
  
  retryLevel(): void {
    localStorage.setItem('level', this.level.toString());
    this.router.navigate(['/operation']);
  }
  restartQuiz(): void { 
    localStorage.setItem('level', this.level.toString());
    this.router.navigate(['/operation']);
  }
  retryOperation(): void {
    localStorage.setItem('level', this.level.toString());
    this.router.navigate(['/operation']);
  }
  retrySudoku(): void {
    localStorage.setItem('level', this.level.toString());
    this.router.navigate(['/sudoku']);
  }
  goToOperations(): void {
    localStorage.removeItem('score');
    localStorage.removeItem('answers');
    localStorage.removeItem('questions');
    localStorage.removeItem('operation');
    this.router.navigate(['/operation']);
  }
 
  reviewQuiz() {
    
      this.router.navigate(['/review']);} 
  
  goToNextLevel() {
    const nextLevel = this.level + 1;
    this.level = nextLevel;
    localStorage.setItem('level', nextLevel.toString());
    localStorage.setItem('operation', this.operation);

    // ✅ Call backend to start session for next level
    this.quizService.startSession(this.operation, nextLevel).subscribe({
      next: (res) => {
        console.log('Session started for next level:', res);
        this.router.navigate(['/operation']);
      },
      error: (err) => {
        console.error('Failed to start session for next level:', err);
        // Fallback to local navigation if API call fails
        this.router.navigate([`/operation/${this.operation}/${this.level}`]);
      }
    });
  }
  reviewAnswers(): void {
    this.router.navigate(['/review']);
  }
  retrySameLevel(): void {
    localStorage.setItem('operation', 'this.operation');
    localStorage.setItem('level', this.level.toString());
    console.log('🔄 Retrying same level:', this.level);
    console.log('🔄 Retrying same operation:', '/operation/${this.operation}/${level}');
    this.router.navigate([`/operation/${this.operation}/${this.level}`]);
  }
  
}
