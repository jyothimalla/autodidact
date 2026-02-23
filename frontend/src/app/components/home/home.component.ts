import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { LoginComponent } from '../../auth/login/login.component';
import { RegisterComponent } from '../../auth/register/register.component';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';


@Component({
  selector: 'app-home',
  standalone: true,
  templateUrl: './home.component.html',
  imports: [CommonModule, FormsModule, MatDialogModule, LoginComponent, RegisterComponent],
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  username: string = '';
  showLogin = false;
  showRegister = false;
  musicOn: boolean = false; // Initialize musicOn to false
  musicSrc: string = 'assets/sounds/music1.mp3'; // Path to your audio file
  
  constructor(private router: Router , private dialog: MatDialog) {}

  openLogin(): void {
    this.dialog.open(LoginComponent, { width: '400px' });
  }

  openRegister(): void {
    this.dialog.open(RegisterComponent, { width: '400px' });
  }
  

  closeModals() {
    this.showLogin = false;
    this.showRegister = false;
  }


  errorMessage = '';

  startQuiz() {
    if (!this.username.trim()) {
      this.errorMessage = 'Please enter your name to start the Quiz!';
      return;
    }

    this.errorMessage = ''; // clear old errors

    localStorage.setItem('username', this.username);
    this.router.navigate(['/operation']);

  }
  continueAsGuest(): void {
    localStorage.setItem('username', 'Guest');
    localStorage.setItem('user_id', '0');
    this.router.navigate(['/operation']);
  }
}
