import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { Router } from '@angular/router';
import { PLATFORM_ID } from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { FooterComponent } from "../footer/footer.component";

@Component({
  selector: 'app-result',
  standalone: true,
  imports: [CommonModule, FooterComponent],
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss']
})
export class ResultComponent implements OnInit {
  platformId = inject(PLATFORM_ID);

  userName: string = '';
  score: number = 0;
  total: number = 0;
  userAnswers: string[] = [];
  questions: any[] = [];
  explanation: string = '';
  operation: string = '';
  level: number = 0;

  get attemptedCount(): number {
    return this.userAnswers.filter(ans => ans && ans.trim() !== '').length;
  }

  constructor(private router: Router, private quizService: QuizService) {}

  ngOnInit(): void {
    const isBrowser = typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  
    if (isBrowser) {
      const name = localStorage.getItem('userName');
      const storedScore = localStorage.getItem('score');
      const storedAnswers = localStorage.getItem('answers');
      const storedQuestions = localStorage.getItem('questions');
      const storedExplanation = localStorage.getItem('explanation');
      const operation = localStorage.getItem('operation') || 'addition';
      const level = parseInt(localStorage.getItem('level') || '0', 10);
  
      this.operation = operation;
      this.level = level;
  
      if (!name || !storedScore || !storedAnswers || !storedQuestions) {
        this.router.navigate(['/']);
        return;
      }
  
      try {
        this.userName = name;
        this.score = parseInt(storedScore);
        this.userAnswers = JSON.parse(storedAnswers);
        this.questions = JSON.parse(storedQuestions);
        this.total = this.questions.length;
      } catch (err) {
        console.error("❌ Failed to parse stored data:", err);
        this.router.navigate(['/']);
      }
  
      this.questions.forEach((q, i) => {
        if (!q.correctValue && q.answer) {
          q.correctValue = q.answer;
        }
      });
  
      if (this.score === 10) {
        const progressKey = `${operation}_progress`;
        const currentUnlocked = parseInt(localStorage.getItem(progressKey) || '0', 10);
        if (level >= currentUnlocked) {
          localStorage.setItem(progressKey, (level + 1).toString());
        }
      }
    } else {
      console.warn("⚠️ Skipping localStorage logic — running on server.");
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
    localStorage.setItem('level', nextLevel.toString());
    localStorage.setItem('operation', this.operation);
    const userName = localStorage.getItem('userName') || 'Guest';

    // ✅ Call backend to start session for next level
    this.quizService.startSession(userName, this.operation, nextLevel).subscribe({
      next: (res) => {
        console.log('Session started for next level:', res);
        this.router.navigate(['/operation']);
      },
      error: (err) => {
        console.error('Failed to start session for next level:', err);
        // Fallback to local navigation if API call fails
        this.router.navigate(['/operation']);
      }
    });
  }
  reviewAnswers(): void {
    this.router.navigate(['/review']);
  }
  retrySameLevel(): void {
    localStorage.setItem('operation', 'addition');
    localStorage.setItem('level', this.level.toString());
    this.router.navigate(['/addition']);  // ✅ go back to addition component
  }
  
}
