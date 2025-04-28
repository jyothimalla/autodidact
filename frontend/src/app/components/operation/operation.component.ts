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
    console.log('🧪 Selected level:', level);

    const operation = this.selectedOperation.toLowerCase();
    localStorage.setItem('operation', operation);
    localStorage.setItem('level', level.toString());

    const directRoutes = ['addition', 'subtraction', 'multiplication', 'division', 'fmc', 'sudoku'];

    if (directRoutes.includes(operation)) {
      console.log('🔄 Navigating to direct route:', operation);
      this.selectedLevel = level;
      this.activeLevel = level;
      this.subLevels = Array.from({ length: 10 }, (_, i) => i);
      console.log('🔄 Sublevels:', this.subLevels);
      console.log('✅ Level selected. Choose a sublevel next.');
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


selectSubLevel(type: 'learn' | 'practice' | 'attempt') {
  this.selectedSublevelType = type;
  this.actionLabel = type === 'learn' ? 'Learn'
                   : type === 'practice' ? 'Practice'
                   : 'Attempt';

  if (this.selectedLevel === null && this.activeLevel !== null) {
  this.selectedLevel = this.activeLevel;
  }
  const subLevel = this.selectedSubLevel !== null ? this.selectedSubLevel : 0;
  console.log('🧩 Sublevel selected:', subLevel);
  const operation = this.selectedOperation.toLowerCase();
  const level = this.selectedLevel;

  const routeMap: Record<number, string> = {
    1: `/learn/${operation}`,   // Learn
    2: `/practice`,             // Try Out
    3: `/${operation}`          // Challenge
  };

  const route = routeMap[subLevel];
  console.log('🔄 Navigating to route:', route);
  console.log('🔄 Sublevel:', subLevel);

  this.router.navigate([route], {
    queryParams: {
      level,
      username: this.username,
      user_id: this.user_id,
      sublevel: subLevel
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
  this.router.navigate([`/practice`], {
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
    this.router.navigate(['/practice'], {
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
