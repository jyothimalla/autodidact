import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { environment } from '../../../environments/environment';
import { ConfigService } from '../../services/config.service';
import { Optional } from '@angular/core';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})

export class RegisterComponent {
  readonly yearOptions = Array.from({ length: 13 }, (_, i) => `Year ${i + 1}`);
  private readonly studentYearStorageKey = 'student_year';
  private readonly analyticsYearStorageKey = 'analytics_year_level';
  registerForm: FormGroup;
  errorMessage: string = '';
  successMessage: string = '';
  isSubmitting = false;
  baseUrl: string = '';

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router,
    private config: ConfigService,
    @Optional() public dialogRef: MatDialogRef<RegisterComponent>
  ) {
    this.registerForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      year: ['', Validators.required],
      password: ['', Validators.required],
      confirm_password: ['', Validators.required]
    });

    const isLocal =
      window.location.hostname === 'localhost' ||
      window.location.hostname === '127.0.0.1';
    const defaultApiBase = isLocal ? 'http://localhost:8000' : 'https://api.autodidact.uk';
    const runtimeApiBase =
      this.config.apiBaseUrl ||
      (window as any).APP_CONFIG?.apiBaseUrl ||
      environment.apiBaseUrl ||
      defaultApiBase;
    this.baseUrl = `${runtimeApiBase.replace(/\/+$/, '')}/auth/register`;
  }

  onSubmit(): void {
    this.errorMessage = '';
    this.successMessage = '';
    if (this.registerForm.invalid || this.isSubmitting) return;
    const { username, email, year, password, confirm_password } = this.registerForm.value;
    if (password !== confirm_password) {
      this.errorMessage = 'Passwords do not match';
      return;
    }

    this.isSubmitting = true;

    this.http.post<any>(this.baseUrl, {
      username,
      email,
      year,
      password,
      confirm_password
    }).subscribe({
      next: (res) => {
        this.successMessage = '🎉 Registration successful!';
        localStorage.setItem('username', username);
        localStorage.setItem('user_id', res.user_id.toString());
        const yearNumber = Number(String(year).replace(/[^\d]/g, ''));
        if (yearNumber >= 1 && yearNumber <= 13) {
          localStorage.setItem(this.studentYearStorageKey, String(yearNumber));
          localStorage.setItem(this.analyticsYearStorageKey, String(yearNumber));
        }
        this.isSubmitting = false;

        setTimeout(() => {
          this.dialogRef?.close();
          this.router.navigate(['/operation']);
        }, 1000);
      },
      error: (err) => {
        this.errorMessage = err?.error?.detail || 'Registration failed';
        this.isSubmitting = false;
      }
    });
  }

  closeDialog(): void {
    if (this.dialogRef) {
      this.dialogRef.close();
      return;
    }
    this.router.navigate(['/']);
  }
}
