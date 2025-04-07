import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-level',
  imports: [CommonModule],
  standalone: true,
  templateUrl: './level.component.html',
  styleUrls: ['./level.component.scss']
})
export class LevelComponent implements OnInit {
  levels: number[] = Array.from({ length: 11 }, (_, i) => i); // Levels 0 to 10
  operation: string = '';

  constructor(private router: Router) {}

  ngOnInit(): void {
    const storedOperation = localStorage.getItem('selectedOperation');
    if (storedOperation) {
      this.operation = storedOperation;
    }
  }

  selectLevel(level: number) {
    localStorage.setItem('selectedLevel', level.toString());
    this.router.navigate(['/quiz']);
  }
}
