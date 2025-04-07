import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-sudoku',
  templateUrl: './sudoku.component.html',
  styleUrls: ['./sudoku.component.scss'],
  standalone: true,
  imports: [CommonModule],
})
export class SudokuComponent implements OnInit {
  grid: number[][] = [];
  fixedCells: boolean[][] = [];

  ngOnInit(): void {
    this.generateSudoku();
  }
  difficulty = 'easy';
  generateSudoku(): void {
    this.grid = Array.from({ length: 9 }, () => Array(9).fill(0));
    this.fixedCells = Array.from({ length: 9 }, () => Array(9).fill(false));

    this.fillDiagonal();
    this.solveSudoku();

    // Remove values to make it Easy (at least 40 clues remain)
    let clues = 0;
    let keepClues = 40;
    if (this.difficulty === 'easy') keepClues = 50;
    else if (this.difficulty === 'medium') keepClues = 35;
    else if (this.difficulty === 'hard') keepClues = 25;
        const positions = Array.from({ length: 81 }, (_, i) => i);
    this.shuffle(positions);

    for (const pos of positions) {
      const row = Math.floor(pos / 9);
      const col = pos % 9;
      const backup = this.grid[row][col];
      this.grid[row][col] = 0;

      const copy = this.copyGrid(this.grid);
      if (!this.hasUniqueSolution(copy)) {
        this.grid[row][col] = backup;
        this.fixedCells[row][col] = true;
        clues++;
        if (clues >= keepClues) break;
      }
    }
  }

  fillDiagonal() {
    for (let i = 0; i < 9; i += 3) {
      this.fillBox(i, i);
    }
  }

  fillBox(row: number, col: number) {
    const nums = this.shuffle([...Array(9)].map((_, i) => i + 1));
    let idx = 0;
    for (let i = 0; i < 3; i++)
      for (let j = 0; j < 3; j++)
        this.grid[row + i][col + j] = nums[idx++];
  }

  solveSudoku(): boolean {
    for (let row = 0; row < 9; row++) {
      for (let col = 0; col < 9; col++) {
        if (this.grid[row][col] === 0) {
          for (let num = 1; num <= 9; num++) {
            if (this.isSafe(row, col, num)) {
              this.grid[row][col] = num;
              if (this.solveSudoku()) return true;
              this.grid[row][col] = 0;
            }
          }
          return false;
        }
      }
    }
    return true;
  }

  isSafe(row: number, col: number, num: number): boolean {
    return !this.usedInRow(row, num) &&
           !this.usedInCol(col, num) &&
           !this.usedInBox(row - (row % 3), col - (col % 3), num);
  }

  usedInRow(row: number, num: number): boolean {
    return this.grid[row].includes(num);
  }

  usedInCol(col: number, num: number): boolean {
    return this.grid.some(r => r[col] === num);
  }

  usedInBox(row: number, col: number, num: number): boolean {
    for (let i = 0; i < 3; i++)
      for (let j = 0; j < 3; j++)
        if (this.grid[row + i][col + j] === num) return true;
    return false;
  }

  hasUniqueSolution(grid: number[][]): boolean {
    let count = 0;
    const solve = (): boolean => {
      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          if (grid[r][c] === 0) {
            for (let n = 1; n <= 9; n++) {
              if (this.isSafeCell(grid, r, c, n)) {
                grid[r][c] = n;
                if (solve()) count++;
                grid[r][c] = 0;
                if (count > 1) return false;
              }
            }
            return false;
          }
        }
      }
      return true;
    };
    solve();
    return count === 1;
  }

  isSafeCell(grid: number[][], row: number, col: number, num: number): boolean {
    for (let x = 0; x < 9; x++) {
      if (grid[row][x] === num || grid[x][col] === num) return false;
    }
    const startRow = row - row % 3;
    const startCol = col - col % 3;
    for (let r = 0; r < 3; r++)
      for (let c = 0; c < 3; c++)
        if (grid[startRow + r][startCol + c] === num) return false;
    return true;
  }

  shuffle(array: number[]): number[] {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }

  copyGrid(grid: number[][]): number[][] {
    return grid.map(row => [...row]);
  }

  isThickBottom(index: number): boolean {
    const row = Math.floor(index / 9);
    return row === 2 || row === 5;
  }
  
  isThickRight(index: number): boolean {
    const col = index % 9;
    return col === 2 || col === 5;
  }
  
sudokuMessage: string = '';

/*  
checkSudoku() {
  // Simple logic to check if all cells are filled

  this.board = this.grid.map((row, rowIndex) =>
    row.map((cell, colIndex) => ({
      value: cell,
      fixed: this.fixedCells[rowIndex][colIndex],   
    }))
  );
  const isComplete = this.board.every(cell => cell.value && cell.value !== '');

  if (!isComplete) {
    this.sudokuMessage = '❌ Please fill all cells before submitting.';
    return;
  }

  // Validate Sudoku (you can enhance this)
  const isValid = this.isValidSudoku(); // You need to implement this
  this.sudokuMessage = isValid ? '✅ Sudoku solved correctly!' : '❌ Incorrect Sudoku.';
}
*/
isValidSudoku(): boolean {
  // Validate rows
  for (let row = 0; row < 9; row++) {
    const seen = new Set();
    for (let col = 0; col < 9; col++) {
      const val = this.grid[row][col];
      if (val && (seen.has(val) || val < 1 || val > 9)) return false;
      seen.add(val);
    }
  }

  // Validate columns
  for (let col = 0; col < 9; col++) {
    const seen = new Set();
    for (let row = 0; row < 9; row++) {
      const val = this.grid[row][col];
      if (val && (seen.has(val) || val < 1 || val > 9)) return false;
      seen.add(val);
    }
  }

  // Validate 3x3 blocks
  for (let boxRow = 0; boxRow < 3; boxRow++) {
    for (let boxCol = 0; boxCol < 3; boxCol++) {
      const seen = new Set();
      for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
          const val = this.grid[boxRow * 3 + r][boxCol * 3 + c];
          if (val && (seen.has(val) || val < 1 || val > 9)) return false;
          seen.add(val);
        }
      }
    }
  }

  return true;
}

}
