import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule, ReactiveFormsModule, MatSlideToggleModule, MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  loginForm: FormGroup;
  errorMessage: string = '';
  baseUrl: string = 'http://localhost:8000/auth/login';


  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router,
    public dialogRef: MatDialogRef<LoginComponent>
  ) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) return;

    const { username, password } = this.loginForm.value;
    
    this.http.post<any> (this.baseUrl, {
      username, password
    }).subscribe({
      next: (res) => {
        localStorage.setItem('username', res.username);

        localStorage.setItem('user_id', res.user_id.toString());
        alert(`✅ Welcome, ${res.username} (ID: ${res.user_id})!`);

        this.dialogRef.close();
        this.router.navigate(['/operation'], {
          queryParams: {username: res.username, user_id: res.user_id }
        });
      },
      error: (err) => {
        console.error('❌ Login failed:', err);
        this.errorMessage = err?.error?.detail || 'Login failed';
      }
    });
  }
}