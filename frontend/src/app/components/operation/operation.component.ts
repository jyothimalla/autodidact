import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { QuizService } from '../../services/quiz.service';
import { query } from 'express';

@Component({
  selector: 'app-operation',
  templateUrl: './operation.component.html',
  imports: [CommonModule],
  standalone: true,
  styleUrls: ['./operation.component.scss']
})
export class OperationComponent implements OnInit {
  operations: string[] = ['Addition', 'Subtraction', 'Multiplication', 'Division', 'FMC', 'Sudoku'];
  selectedOperation: string = '';
  levels: number[] = [];
  unlockedLevel = 0;
  username: string = '';
  user_id: number = 0;

  sudokuLevels = [
    { label: 'Easy', value: 0 },
    { label: 'Medium', value: 1 },
    { label: 'Difficult', value: 2},
  ];
  
  constructor(private router: Router, private quizService: QuizService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.username = this.route.snapshot.queryParams['username'] || localStorage.getItem('username') || '';
    this.user_id = parseInt(localStorage.getItem('user_id') || '0', 10);

    if(!this.username || !this.user_id) {
      alert("⚠️ You must be logged in to start the quiz.");
      this.router.navigate(['/login']);
    }
    this.route.paramMap.subscribe(params => {
      this.selectedOperation = params.get('type') || '';
      if (!this.selectedOperation) {
        this.levels = []; // ⛔️ Hide levels if operation is not selected
      } else {
        this.setLevelsBasedOnOperation();
      }
    });
  }
  setLevelsBasedOnOperation(): void {
    const operation = this.selectedOperation.toLowerCase();
    const progressKey = `${operation}_progress`;

    this.unlockedLevel =
    this.username === 'Guest'
    ? 0
    : parseInt(localStorage.getItem(`${operation}_progress`) || '0', 10);

    this.levels = operation === 'sudoku'
      ? this.sudokuLevels.map(l => l.value)
      : Array.from({ length: 10 }, (_, i) => i);
  }
  

    selectOperation(operation: string) {
    
      this.selectedOperation = operation;
      console.log('🧠 Operation clicked:', operation);

      const progressKey = `${operation.toLowerCase()}_progress`;
      this.unlockedLevel = parseInt(localStorage.getItem(progressKey) || '0', 10);
      console.log('🔓 Unlocked level:', this.unlockedLevel);
    
      // localStorage.setItem('selectedOperation', operation.toLowerCase());
    
      this.levels = operation.toLowerCase() === 'sudoku'
        ? this.sudokuLevels.map(lvl => lvl.value)
        : Array.from({ length:10 }, (_, i) => i);  // Try limiting to 3 levels for now
    
      console.log('📋 Available levels:', this.levels);
    }
    

  isLevelLocked(level: number): boolean {
  return this.username === 'Guest' ? level !== 0 : level > this.unlockedLevel;
  }

selectLevel(level: number) {

  if (this.isLevelLocked(level)) {
    console.warn(`🚫 Level ${level} is locked!`);
    return;
  }
  console.log('🧪 Selected level:', level);

  const operation = this.selectedOperation.toLowerCase();
  localStorage.setItem('operation', operation);
  localStorage.setItem('level', level.toString());

  const directRoutes = ['addition', 'subtraction', 'multiplication', 'division', 'fmc', 'sudoku'];

  if (directRoutes.includes(operation)) {
    console.log('🔄 Navigating to direct route:', operation);
    this.navigateToOperation(operation, level);
  }
   else {
    this.quizService.startSession(operation, level).subscribe({
      next: () => {
        console.log('✅ Session started, navigating to /quiz');
        this.router.navigate(['/quiz']);
      },
      error: (err) => {
        console.error('❌ Failed to start session:', err);
        alert('Could not start quiz session. Please try again.');
      }
    });
  }
}
navigateToOperation(operation: string, level: number) {
  this.router.navigate([`/${operation}`], {
    queryParams: {
      level,
      username: this.username,
      user_id: this.user_id
    }
  });
}

   
  getLevelLabel(level: number): string {
    if (this.selectedOperation.toLowerCase() === 'sudoku') {
      const found = this.sudokuLevels.find(l => l.value === level);
      return found ? found.label : `Level ${level}`;
    }
    return `Level ${level}`;
  }
}
