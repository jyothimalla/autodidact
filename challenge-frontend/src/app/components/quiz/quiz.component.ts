import { Component, OnInit } from '@angular/core';
import { QuizService } from '../../services/quiz.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SudokuComponent } from "../sudoku/sudoku.component";

@Component({
  selector: 'app-quiz',
  imports: [CommonModule, FormsModule, SudokuComponent],
  templateUrl: './quiz.component.html',
  styleUrls: ['./quiz.component.scss'],
  standalone: true,
})
export class QuizComponent implements OnInit {
  userName = '';
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

  constructor(private quizService: QuizService, private router: Router) {}

  ngOnInit(): void {
    const storedName = localStorage.getItem('userName');
    const operation = localStorage.getItem('operation') || 'addition';
    const level = parseInt(localStorage.getItem('level') || '0', 10);
    
    if (operation === 'sudoku') {
      this.isSudoku = true;
      this.router.navigate(['/sudoku']);
      return; // no need to call quizService for questions
    }
    if (storedName) {
      this.userName = storedName;
      this.currentOperation = operation;
      this.quizService.getQuestions(this.userName).subscribe(data => {
        this.questions = data;
        this.startTimer();
      });
    } else {
      this.router.navigate(['/']);
    }
  }

  startTimer() {
    this.timer = setInterval(() => {
      this.secondsElapsed++;
      const minutes = Math.floor(this.secondsElapsed / 60);
      const seconds = this.secondsElapsed % 60;
      this.elapsedTime = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }, 1000);
  }

  switchOperation(op: string) {
    localStorage.setItem('operation', op);
    window.location.reload(); // force reload with new operation
  }

  submitAnswer() {
    const currentQ = this.questions[this.currentQIndex];
    const correctAnswer = currentQ.options[currentQ.answer];
    const userAnswer = this.answerInput.trim();
  
    // Score and feedback logic
    if (userAnswer === correctAnswer) {
      this.score++;
      this.feedbackMessage = `✅ Correct! Good job!`;
    } else {
      this.feedbackMessage = `❌ Incorrect!\nCorrect answer is: ${correctAnswer}\nYour answer: ${userAnswer}\nExplanation: ${currentQ.explanation || 'N/A'}`;
    }
  
    // Save user's answer
    this.userAnswers[this.currentQIndex] = userAnswer;
    this.answerInput = '';
    this.attemptedCount++;
  
    // Move to next question or finish
    if (this.currentQIndex < this.questions.length - 1) {
      this.currentQIndex++;
    } else {
      // ✅ Save everything before navigating
      localStorage.setItem('score', this.score.toString());
      localStorage.setItem('answers', JSON.stringify(this.userAnswers));
      this.questions.forEach((q, i) => {
        const correctValue = q.options[q.answer]; // e.g., "12"
        const explanation = q.explanation || '';
        q.correctValue = correctValue;
      });
      localStorage.setItem('questions', JSON.stringify(this.questions));
      localStorage.setItem('explanation', currentQ.explanation || '');
  
      // ✅ Navigate to result
      this.router.navigate(['/result']);
    }
  }
  
  restartQuiz() {
    this.router.navigate(['/operation']);
  }
  
}
