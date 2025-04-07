import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  imports: [CommonModule, FormsModule],
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  userName: string = '';

  constructor(
    private router: Router
  ) {}

  errorMessage = '';

  startQuiz() {
    if (!this.userName.trim()) {
      this.errorMessage = 'Please enter your name to start the Quiz!';
      return;
    }

    this.errorMessage = ''; // clear old errors

    localStorage.setItem('userName', this.userName);
    this.router.navigate(['/operation']);

  }

}
