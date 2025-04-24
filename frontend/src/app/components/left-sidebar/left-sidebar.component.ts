import { Component, OnInit } from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-left-sidebar',
  imports: [CommonModule, FormsModule],
  templateUrl: './left-sidebar.component.html',
  styleUrls: ['./left-sidebar.component.scss'],
  standalone: true,
})

export class LeftSidebarComponent implements OnInit {
  username = '';
  questions: any[] = [];
  currentQIndex = 0;
  currentOperation = '';
  answerInput: string = '';
  score = 0;
  attemptedCount = 0;
  feedbackMessage = '';
  explanation = '';
  elapsedTime = '0:00';
  userAnswers: string[] = [];
  quizCompleted = false;
  level: number = 0;
  isSudoku: boolean = false;
  private timer: any;
  private secondsElapsed = 0;
  user_id: number = 0;
  ninjaStars: number = 0;
  currentLevelProgress: { total_attempts: number, best_score: number } | null = null;

  constructor(private quizService: QuizService, private router: Router, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.username = params['username'] || localStorage.getItem('username') || '';
      this.user_id = parseInt(params['user_id'] || localStorage.getItem('user_id') || '0', 10);
      this.level = parseInt(params['level'] || '0', 10);     
      const operation = localStorage.getItem('operation') || 'addition';
  
      // ✅ Call backend API to fetch progress
      this.quizService.getUserProgressByOperation(operation).subscribe({
        next: (res) => {
          console.log('📊 Progress Data:', res);
  
          this.ninjaStars = res.ninja_stars || 0;
  
          // Get data for the current level
          const levelProgress = res.progress?.find((p: any) => p.level === this.level);
          if (levelProgress) {
            this.currentLevelProgress = {
              total_attempts: levelProgress.attempts || 0,
              best_score: levelProgress.best_score || 0,
            };
          }
        },
        error: (err) => {
          console.error('❌ Failed to load user progress:', err);
        }
      });
    });
  }
  
  startTimer() {
    this.timer = setInterval(() => {
      this.secondsElapsed++;
      const minutes = Math.floor(this.secondsElapsed / 60);
      const seconds = this.secondsElapsed % 60;
      this.elapsedTime = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }, 1000);
  }

switchOperation(operation: string) {
  this.currentOperation = operation;
  localStorage.setItem('operation', operation);
  this.router.navigate(['/addition']);
  this.quizService.getQuestions(this.username).subscribe(data => {
    this.questions = data;
    this.startTimer();
  }
  );
  this.router.navigate(['/addition']);
  this.quizService.getQuestions(this.username).subscribe(data => {
    this.questions = data;
    this.startTimer();
  }
  );
  
}


}
