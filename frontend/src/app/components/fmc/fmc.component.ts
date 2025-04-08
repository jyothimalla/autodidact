import { Component , OnInit,  HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';  // ✅ this is required
import { WordProblemService, WordProblem } from '../../services/word-problem.service';
import { HeaderComponent } from "../header/header.component";
import { LeftSidebarComponent } from "../left-sidebar/left-sidebar.component";
import { FooterComponent } from "../footer/footer.component";
import { RightSidebarComponent } from '../right-sidebar/right-sidebar.component';

@Component({
  selector: 'app-fmc',
  standalone: true,
  imports: [CommonModule, FormsModule, HeaderComponent, LeftSidebarComponent, FooterComponent, RightSidebarComponent],  // ✅ enable form handling
  templateUrl: './fmc.component.html',
  styleUrls: ['./fmc.component.scss']
})
export class FmcComponent {
  questions: WordProblem[] = [];
  currentQIndex = 0;
  userAnswer: string = '';
  
  userName: string = '';
  score: number = 0;
  isFinished: boolean = false;
  correctAnswers: string[] = [];
  isEnterDisabled: boolean = false; // Flag to prevent rapid fire
  lastUserAnswer: string = '';
  lastCorrectAnswer: string = '';
  isCorrect: boolean = true; 
  elapsedTime: string = '0:00';

  constructor(private wordService: WordProblemService) {}
  
  ngOnInit(): void {
    console.log('✅ FMC component loaded');
    this.loadProblems();
  }
  
  loadProblems(): void {
    this.wordService.getWordProblems('Jyothi', 'addition', 2).subscribe({
      next: (questions: WordProblem[]) => {
        this.questions = questions;  // ✅ Important
        this.currentQIndex = 0;
        this.score = 0;
        this.userAnswer = '';
        this.isFinished = false;
      },
      error: (err) => {
        console.error('❌ Failed to load word problems:', err);
      }
    });
  }
  

  submitAnswer(): void {
    const correct = this.questions[this.currentQIndex].answer.trim();
    const isCorrect = this.userAnswer.trim() === correct;
    this.correctAnswers.push(correct);
    if (isCorrect) this.score++;

    this.userAnswer = '';
    this.currentQIndex++;

    if (this.currentQIndex >= this.questions.length) {
      this.isFinished = true;
    }
  }
  @HostListener('document:keydown.enter', ['$event'])
  
  handleEnter(event: KeyboardEvent) {
  if (!this.isEnterDisabled) {
    this.isEnterDisabled = true;  // Prevent rapid fire
    this.submitAnswer();

    // Reset after short delay
    setTimeout(() => {
      this.isEnterDisabled = false;
    }, 11500);  // Adjust timing if needed
  }
}


  tryAgain(): void {
    this.loadProblems();
  }
}
