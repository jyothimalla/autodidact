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
  subLevels: number[] = [];
  selectedSubLevel: number | null = null;
  activeLevel: number | null = null;
  selectedLevel: number | null = null;
  isSudoku: boolean = false;
  actionLabel: string | null = null;
  selectedSublevelType: 'learn' | 'practice' | 'attempt' | null = null;

  sudokuLevels = [
    { label: 'Easy', value: 0 },
    { label: 'Medium', value: 1 },
    { label: 'Difficult', value: 2 },
  ];

  constructor(private router: Router, private quizService: QuizService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.username = this.route.snapshot.queryParams['username'] || localStorage.getItem('username') || '';
    this.user_id = parseInt(localStorage.getItem('user_id') || '0', 10);

    if (!this.username || !this.user_id) {
      alert("⚠️ You must be logged in to start the quiz.");
      this.router.navigate(['/login']);
    }

    this.route.paramMap.subscribe(params => {
      this.selectedOperation = params.get('type') || '';
      if (!this.selectedOperation) {
        this.levels = [];
      } else {
        this.setLevelsBasedOnOperation();
      }
    });
  }

  setLevelsBasedOnOperation(): void {
    const operation = this.selectedOperation.toLowerCase();
    const progressKey = `${operation}_progress`;
    this.unlockedLevel = this.username === 'Guest'
      ? 0
      : parseInt(localStorage.getItem(progressKey) || '0', 10);
    this.levels = operation === 'sudoku'
      ? this.sudokuLevels.map(l => l.value)
      : Array.from({ length: 10 }, (_, i) => i);
  }

  selectOperation(operation: string) {
    this.selectedOperation = operation;
    const progressKey = `${operation.toLowerCase()}_progress`;
    this.unlockedLevel = parseInt(localStorage.getItem(progressKey) || '0', 10);
    this.levels = operation.toLowerCase() === 'sudoku'
      ? this.sudokuLevels.map(lvl => lvl.value)
      : Array.from({ length: 10 }, (_, i) => i);
  }

  isLevelLocked(level: number): boolean {
    return this.username === 'Guest' ? level !== 0 : level > this.unlockedLevel;
  }

  selectLevel(level: number): void {
    if (this.isLevelLocked(level)) return;
    this.selectedLevel = level;
    this.activeLevel = level;
    localStorage.setItem('operation', this.selectedOperation.toLowerCase());
    localStorage.setItem('level', level.toString());
  }

  selectSubLevel(type: 'learn' | 'practice' | 'attempt' | null): void {
    this.selectedSublevelType = type;
    this.actionLabel = type === 'learn' ? 'Learn' : type === 'practice' ? 'Practice' : 'Attempt';
  }

  confirmAction(): void {
    const operation = this.selectedOperation.toLowerCase();
    const level = this.selectedLevel;

    const routeMap: Record<string, string> = {
      'Learn': `/learn/${operation}`,
      'Practice': `/practice/${operation}`,
      'Attempt': `/${operation}`
    };

    const selectedRoute = routeMap[this.actionLabel || ''] || '/operation';
    const queryParams: any = {
      level,
      username: this.username,
      user_id: this.user_id
    };
    if (this.actionLabel === 'Practice') {
      queryParams.operation = operation;
    }

    this.router.navigate([selectedRoute], { queryParams });
    this.resetConfirmation();
  }

  cancelAction(): void {
    this.resetConfirmation();
  }

  resetConfirmation(): void {
    this.actionLabel = null;
    this.selectedSublevelType = null;
  }

  getLevelLabel(level: number): string {
    if (this.selectedOperation.toLowerCase() === 'sudoku') {
      const found = this.sudokuLevels.find(l => l.value === level);
      return found ? found.label : `Level ${level}`;
    }
    return `Level ${level}`;
  }

  onLevelClick(level: number): void {
    if (!this.isLevelLocked(level)) {
      this.selectedLevel = level;
    }
  }

  startPractice(level: number): void {
    this.selectedLevel = level;
    this.actionLabel = 'Practice';
    this.selectedSublevelType = 'practice';
  }

  startLearning(level: number): void {
    this.selectedLevel = level;
    this.actionLabel = 'Learn';
    this.selectedSublevelType = 'learn';
  }

  startAttempt(level: number) {
    this.selectedLevel = level;
    this.actionLabel = 'Attempt';
    this.selectedSublevelType = 'attempt';
  }

  navigateToOperation(): void {
    this.router.navigate([`/${this.selectedOperation.toLowerCase()}`], {
      queryParams: {
        sublevel: this.subLevels,
        username: this.username,
        user_id: this.user_id
      }
    });
  }

  navigateToLearn(): void {
    if (this.activeLevel === null) return;
    this.router.navigate([`/learn/${this.selectedOperation.toLowerCase()}`], {
      queryParams: {
        level: this.activeLevel,
        username: this.username,
        user_id: this.user_id
      }
    });
  }

  navigateToPractice(): void {
    if (this.activeLevel === null) return;
    this.router.navigate([`/practice/${this.selectedOperation.toLowerCase()}`], {
      queryParams: {
        level: this.activeLevel,
        operation: this.selectedOperation.toLowerCase(),
        username: this.username,
        user_id: this.user_id
      }
    });
  }

  navigateToChallenge(): void {
    if (this.activeLevel === null) return;
    this.router.navigate([`/${this.selectedOperation.toLowerCase()}`], {
      queryParams: {
        level: this.activeLevel,
        username: this.username,
        user_id: this.user_id
      }
    });
  }
}
