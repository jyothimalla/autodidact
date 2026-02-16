import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { Router } from '@angular/router';
import { Injectable } from '@angular/core';


@Component({
  selector: 'app-admin-login',
  templateUrl: './admin-login.component.html',
  styleUrls: ['./admin-login.component.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule],

})
export class AdminLoginComponent {
  username: string = '';
  password: string = '';
  showPassword: boolean = false;
  loginError: string = '';

  constructor(private http: HttpClient) {}

  togglePassword(): void {
    this.showPassword = !this.showPassword;
  }

  login(): void {
    this.loginError = '';
    this.http.post('/admin/login', {
      username: this.username,
      password: this.password
    }).subscribe({
      next: () => {
        alert('✅ Login successful');
        window.location.href = '/admin/dashboard';
      },
      error: () => {
        this.loginError = 'Invalid credentials. Please try again.';
      }
    });
  }

  toggleDarkMode(event: any): void {
    document.body.classList.toggle('dark-mode', event.target.checked);
  }
}