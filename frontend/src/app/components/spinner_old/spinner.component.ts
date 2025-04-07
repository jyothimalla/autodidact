import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { QuizService } from '../../services/quiz.service';
@Component({
  selector: 'app-spinner',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './spinner.component.html',
  styleUrl: './spinner.component.scss'
})
export class SpinnerComponent {
  labels = ['Spin Again', 'Addition', 'Subtraction', 'Multiplication', 'Division', 'FMC', 'Sudoku'];
  spinning = false;
  selectedLabel = '';
  showResult = false;

  constructor(private router: Router,
    private quizService: QuizService
  ) {}

  spinWheel() {
    this.spinning = true;
    this.showResult = false;
    this.selectedLabel = '';
    
    const sliceAngle = 360 / this.labels.length;
    const spinDegrees = 360 * 5 + Math.floor(Math.random() * 360);
    const wheel = document.querySelector('.wheel') as HTMLElement;
  
    wheel.style.transition = 'transform 3s ease-out';
    wheel.style.transform = `rotate(${spinDegrees}deg)`;
  
    // Calculate selected label after spin animation
    setTimeout(() => {
      const finalDegrees = spinDegrees % 360;
      const sliceAngle = 360 / this.labels.length;

      const adjustedDegrees = (360 - finalDegrees - sliceAngle / 2 + 360) % 360;
      const selectedIndex = Math.floor(adjustedDegrees / sliceAngle) % this.labels.length;


      this.selectedLabel = this.labels[selectedIndex];

      this.showResult = true;
      this.spinning = false;
  
      console.log('✅ Selected Label:', this.selectedLabel);
  
      if (this.selectedLabel !== 'Spin Again') {
        const userName = localStorage.getItem('userName') || '';
  
        this.quizService.startSession(userName, this.selectedLabel.toLowerCase()).subscribe({
          next: () => {
            localStorage.setItem('operation', this.selectedLabel.toLowerCase());
  
            setTimeout(() => {
              this.router.navigate(['/quiz']);
            }, 3000);
          },
          error: (err: any) => {
            console.error('❌ Failed to start session:', err);
          }
        });
      } else {
        setTimeout(() => {
          this.showResult = false;
        }, 3000);
      }
    }, 3000); // Wait for spin animation to finish
  }
  
}