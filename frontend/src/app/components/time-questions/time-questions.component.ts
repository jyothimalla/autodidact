import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';
import { RightSidebarComponent } from '../right-sidebar/right-sidebar.component';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-time-questions',
  imports: [CommonModule, FormsModule, LeftSidebarComponent, RightSidebarComponent],
  templateUrl: './time-questions.component.html',
  styleUrl: './time-questions.component.scss',
  standalone: true
})
export class TimeQuestionsComponent implements OnInit {
  hour: number = 0;
  minute: number = 0;
  userAnswer: string = '';
  feedback: string = '';
  hourHand = { x: 0, y: 0 };
  minuteHand = { x: 0, y: 0 };
  secondHand = {x:0, y:0};
  second: number = 0;
  secondAngle: number = 0;
  score: number = 0;
  showFeedback: boolean = false;
  currentQuestion: number = 1;
  totalQuestions: number = 10;
  quizEnded: boolean = false;
  elapsedTime = '0:00';
  private timer: any;
  private secondsElapsed = 0;

  constructor(private http: HttpClient) {}

  minuteTicks = Array.from({ length: 60 }, (_, i) => i);

  hourMarks = Array.from({ length: 12 }, (_, i) => {
    const angle = (i + 1) * 30;
    const rad = (angle * Math.PI) / 180;
    return {
      label: i + 1,
      x: 150 + 125 * Math.sin(rad),
      y: 150 - 125 * Math.cos(rad)
    };
  });
  ngOnInit(): void {
    this.generateRandomTime();
    this.startTimer();
  }

  generateRandomTime(): void {
    this.hour = Math.floor(Math.random() * 12); // 0 to 11
    this.minute = Math.floor(Math.random() * 60); // 0 to 59
    this.second = Math.floor(Math.random()*60);
    console.log(
      `Generated time: ${this.hour.toString().padStart(2, '0')}:${this.minute
        .toString()
        .padStart(2, '0')} | seconds: ${this.second}`
    );
    
    this.calculateHandPositions();
  }
  saveToDatabase(): void {
    const payload = {
      user_id: 1, // ← get from login/session
      user_name: 'testuser', // ← same
      score: this.score,
      total_questions: this.totalQuestions
    };
  
    this.http.post(`${environment.apiBaseUrl}/time-quiz/submit/`, payload).subscribe({
      next: res => console.log('✅ Saved:', res),
      error: err => console.error('❌ Error:', err)
    });
  }
  calculateHandPositions(): void {
    const hourAngle = ((this.hour % 12) + this.minute / 60) * 30;
    const minuteAngle = this.minute * 6;
    const secondAngle = this.second * 6;

    this.hourHand = this.calculateHandEnd(hourAngle, 60);
    this.minuteHand = this.calculateHandEnd(minuteAngle, 90);
    this.secondHand = this.calculateHandEnd(secondAngle, 100);
  }

  calculateHandEnd(angle: number, length: number): { x: number; y: number } {
    const rad = (angle * Math.PI) / 180;
    return {
      x: 150 + length * Math.sin(rad),
      y: 150 - length * Math.cos(rad)
    };
  }
  
  restartQuiz(): void {
    this.currentQuestion = 1;
    this.score = 0;
    this.quizEnded = false;
    this.userAnswer = '';
    this.feedback = '';
    this.generateRandomTime();
  }
  
  updateClockHands(hour: number, minute: number, second: number): void {
    const hourAngle = (hour % 12 + minute / 60) * 30;
    const minuteAngle = minute * 6;
    const secondAngle = second * 6;
  
    this.hourHand = {
      x: this.getX(hourAngle, 60),
      y: this.getY(hourAngle, 60)
    };
    this.minuteHand = {
      x: this.getX(minuteAngle, 90),
      y: this.getY(minuteAngle, 90)
    };
    this.secondHand = {
      x: this.getX(secondAngle, 100),
      y: this.getY(secondAngle, 100)
    };
    
  }
  startTimer(): void {
    this.timer = setInterval(() => {
      this.secondsElapsed++;
      const minutes = Math.floor(this.secondsElapsed / 60);
      const seconds = this.secondsElapsed % 60;
      this.elapsedTime = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }, 1000);
  }
  getFormattedTime(hour: number, minute: number): string {
    const h = hour;
    const m = minute < 10 ? '0' + minute : minute;
    return `${h}:${m}`;
  }
  checkAnswer(): void {
    const normalize = (input: string): string => {
      let parts = input.trim().split(':');
      let hour = parseInt(parts[0], 10);
      let minute = parseInt(parts[1] || '0', 10);
      return `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
    
    };
    
    const userTime = normalize(this.userAnswer);
    const correctTime = `${this.hour.toString().padStart(2, '0')}:${this.minute.toString().padStart(2, '0')}`;
  
    if (userTime === correctTime) {
      this.feedback = '✅ Correct!';
      this.score++;
    } else {
      this.feedback = `❌ Incorrect. Correct answer: ${correctTime}`;
    }
  
    this.showFeedback = true;
  
    setTimeout(() => {
      this.showFeedback = false;
      this.userAnswer = '';
      if (this.currentQuestion < this.totalQuestions) {
        this.currentQuestion++;
        this.generateRandomTime();
      } else {
        this.quizEnded = true;
      }
    }, 2000);
    if (this.currentQuestion >= this.totalQuestions) {
      this.quizEnded = true;
      this.saveToDatabase(); // 👈 save attempt
    }
  }
  
  nextQuestion(): void {
    this.userAnswer = '';
    this.feedback = '';
    this.showFeedback = false;
  
    if (this.currentQuestion < this.totalQuestions) {
      this.currentQuestion++;
      this.generateRandomTime();
    } else {
      this.quizEnded = true;
    }
  }
  
  get secondHandX(): number {
    return 50 + 40 * Math.sin(this.second * 6 * Math.PI / 180);
  }
  
  get secondHandY(): number {
    return 50 - 40 * Math.cos(this.second * 6 * Math.PI / 180);
  }
  getHourAngle(): number {
    return (this.hour % 12 + this.minute / 60) * 30; // each hour = 30°
  }
  getMinuteAngle(): number {
    return this.minute * 6; // each minute = 6°
  }
  getSecondAngle(): number {
    return this.second * 6; // each second = 6°
  }

  getX(angle: number, radius: number): number {
    return 150 + radius * Math.sin(angle * Math.PI / 180);
  }
  
  getY(angle: number, radius: number): number {
    return 150 - radius * Math.cos(angle * Math.PI / 180);
  }
  
  
}