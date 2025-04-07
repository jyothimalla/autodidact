import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { QuizService } from '../../services/quiz.service';

@Component({
  selector: 'app-operation',
  templateUrl: './operation.component.html',
  imports: [CommonModule],
  standalone: true,
  styleUrls: ['./operation.component.scss']
})
export class OperationComponent {
  operations: string[] = ['Addition', 'Subtraction', 'Multiplication', 'Division', 'FMC', 'Sudoku'];
  selectedOperation: string = '';
  levels: number[] = [];
  unlockedLevel = 0;

  sudokuLevels = [
    { label: 'Easy', value: 1 },
    { label: 'Medium', value: 2 },
    { label: 'Difficult', value: 3 },
  ];

  constructor(private router: Router, private quizService: QuizService) {}

  selectOperation(operation: string) {
    this.selectedOperation = operation;

    const progressKey = `${operation.toLowerCase()}_progress`;
    this.unlockedLevel = parseInt(localStorage.getItem(progressKey) || '1', 10);

    localStorage.setItem('selectedOperation', operation.toLowerCase());

    this.levels = operation.toLowerCase() === 'sudoku'
      ? this.sudokuLevels.map(lvl => lvl.value)
      : Array.from({ length: 10 }, (_, i) => i);
  }

  isLevelLocked(level: number): boolean {
    return level > this.unlockedLevel;
  }

  selectLevel(level: number) {
    if (this.isLevelLocked(level)) return;

    const userName = localStorage.getItem('userName') || 'Guest';
    const operation = this.selectedOperation.toLowerCase();

    localStorage.setItem('operation', operation);
    localStorage.setItem('level', level.toString());

    if (operation === 'addition') {
      this.router.navigate(['/addition']);
    } 
    else if (operation === 'subtraction') {
      this.router.navigate(['/subtraction']);
    }
    else if (operation === 'multiplication') {
      this.router.navigate(['/multiplication']);
    }
    else if (operation === 'division') {
      this.router.navigate(['/division']);
    }
    else if (operation === 'fmc') {
      this.router.navigate(['/fmc']);
    }
    else if (operation === 'sudoku') {
      this.router.navigate(['/sudoku']);
    }
    else {
      this.quizService.startSession(userName, operation, level).subscribe({
        next: () => this.router.navigate(['/quiz']),
        error: (err) => console.error('❌ Failed to start session:', err)
      });
    }
  }
   
  getLevelLabel(level: number): string {
      if (this.selectedOperation.toLowerCase() === 'sudoku') {
        const found = this.sudokuLevels.find(l => l.value === level);
        return found ? found.label : `Level ${level}`;
      }
      return `Level ${level}`;
    
  }
}
