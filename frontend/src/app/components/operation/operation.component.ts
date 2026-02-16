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
  operations: string[] = ['Addition', 'Subtraction', 'Multiplication', 'Division', 'FMC', 'Sudoku', 'Time'];
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
  currentOperation: string = '';
  level: number = 0;

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

      const progressKey = `${operation.toLowerCase()}_progress`;
      this.unlockedLevel = parseInt(localStorage.getItem(progressKey) || '0', 10);
      console.log('🔓 Unlocked level:', this.unlockedLevel);
    
      // localStorage.setItem('selectedOperation', operation.toLowerCase());
    
      this.levels = operation.toLowerCase() === 'sudoku'
        ? this.sudokuLevels.map(lvl => lvl.value)
        : Array.from({ length:10 }, (_, i) => i);  // Try limiting to 3 levels for now
    
        console.log('🧠 Operation clicked:', operation);

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

  const operation = this.selectedOperation.toLowerCase();
  this.level = level;

  this.quizService.startSession(this.username, operation, level).subscribe({
    next: () => {
      console.log(`✅ Session started for ${operation} Level ${level}`);
      this.router.navigate([`/${operation}`], {
        queryParams: { level, username: this.username, user_id: this.user_id }
      });
    },
    error: (err) => {
      console.error('❌ Failed to start session:', err);
      alert('Could not start quiz session. Please try again.');
    }
  });
}



selectSubLevel(type: 'learn' | 'practice' | 'attempt' | null): void {
  this.selectedSublevelType = type;
  
  if (type === 'learn' || type === 'practice' || type === 'attempt') {
    this.actionLabel = {
      learn: 'Learn',
      practice: 'Practice',
      attempt: 'Attempt'
    }[type];
  } else {
    this.actionLabel = null;
  }
  

  // Fallback if sublevel not explicitly selected
  const subLevel = this.selectedSubLevel ?? 0;
  const operation = this.selectedOperation?.toLowerCase();
  const level = this.selectedLevel ?? this.activeLevel;

  if (!operation || level === null || !this.actionLabel) {
    console.warn('🚫 Cannot navigate: missing operation or level', { operation, level, subLevel });
    this.router.navigate(['/operation']);
    return;
  }

  // Determine the correct route
  const routeMap: Record<string, string> = {
    Learn: `/learn/${operation}`,
    Practice: `/practice/${operation}`,
    Attempt: `/${operation}`
  };

  const targetRoute = routeMap[this.actionLabel];

  if (!targetRoute) {
    console.warn('⚠️ Invalid navigation target:', this.actionLabel);
    this.router.navigate(['/operation']);
    return;
  }

  console.log(`🔄 Navigating to: ${targetRoute} (Level: ${level})`);

  this.router.navigate([targetRoute], {
    queryParams: {
      operation,
      level,
      sublevel: subLevel,
      username: this.username,
      user_id: this.user_id
    }
  });
}


navigateToOperation(): void {
  const operation = this.selectedOperation.toLowerCase();
  this.router.navigate([`/${operation}`], {
    queryParams: {
      sublevel: this.subLevels,
      username: this.username,
      user_id: this.user_id
    }
  });
}
navigateToLearn(): void {
  const operation = this.selectedOperation.toLowerCase();
  if (this.activeLevel === null) return;
  this.router.navigate([`/learn/${operation}`], {
    queryParams: {
      level: this.activeLevel,
      username: this.username,
      user_id: this.user_id
    }
  });
}

navigateToPractice(): void {
  const operation = this.selectedOperation.toLowerCase();
  if (this.activeLevel === null) return;
  this.router.navigate([`/practice/${operation}`], {
    queryParams: {
      level: this.activeLevel,
      operation,
      username: this.username,
      user_id: this.user_id
    }
  });
}

navigateToChallenge(): void {
  const operation = this.selectedOperation.toLowerCase();
  if (this.activeLevel === null) return;
  this.router.navigate([`/${operation}`], {
    queryParams: {
      level: this.activeLevel,
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

  startPractice(level: number): void {
    const operation = this.selectedOperation.toLowerCase();
    this.selectedLevel = level;
    this.actionLabel = 'Practice';
    this.selectedSublevelType = 'practice';
    this.router.navigate([`/practice/${operation}`], {
      queryParams: {
        level,
        operation,
        username: this.username,
        user_id: this.user_id
      }
    });
  }

  onLevelClick(level: number): void {
    if (!this.isLevelLocked(level)) {
      this.selectedLevel = level;
    } else {
      console.warn(`🚫 Level ${level} is locked.`);
    }
  }
  startLearning(level: number): void {
    const operation = this.selectedOperation.toLowerCase();
    this.selectedLevel = level;
    this.actionLabel = 'Learn';
    this.selectedSublevelType = 'learn';
    console.log(`📘 Starting learning for ${operation}, Level ${level}`);
  
    this.router.navigate([`/learn/${operation}`], {
      queryParams: {
        level: level,
        username: this.username,
        user_id: this.user_id
      }
    });
  }
  startAttempt(level: number) {
    this.selectedLevel = level;
    this.actionLabel = 'Attempt';
    this.selectedSublevelType = 'attempt';
  }

learnLevel(level: number) {
  this.activeLevel = level;
  this.actionLabel = 'Learn';
  // Optionally: route to video or learning page
}

confirmAction(): void {
  const operation = this.selectedOperation.toLowerCase();
  const level = this.selectedLevel;

  const routeMap: Record<string, string> = {
    'Learn': `/learn/${operation}`,
    'Practice': '/practice',
    'Attempt': `/${operation}`
  };

  const selectedRoute = routeMap[this.actionLabel || ''] || '/operation';

  const queryParams: any = {
    level,
    username: this.username,
    user_id: this.user_id
  };

  if (this.actionLabel === 'Practice') {
    queryParams.operation = operation;  // Only Practice needs 'operation' separately
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


}
