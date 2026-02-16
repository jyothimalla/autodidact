import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule
  ],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})

export class RegisterComponent {
  registerForm: FormGroup;
  errorMessage: string = '';
  successMessage: string = '';
  baseUrl: string = `${environment.apiBaseUrl}/auth/register`;

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router,
    public dialogRef: MatDialogRef<RegisterComponent>
  ) {
    this.registerForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      confirm_password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.registerForm.invalid) return;
    const { username, email, password, confirm_password } = this.registerForm.value;

    this.http.post<any>(this.baseUrl, {
      username,
      email,
      password,
      confirm_password
    }).subscribe({
      next: (res) => {
        this.successMessage = '🎉 Registration successful!';
        localStorage.setItem('username', username);
        localStorage.setItem('user_id', res.user_id.toString());

        setTimeout(() => {
          this.dialogRef.close();
          this.router.navigate(['/operation']);
        }, 1000);
      },
      error: (err) => {
        this.errorMessage = err?.error?.detail || 'Registration failed';
      }
    });
  }

  closeDialog() {
    this.dialogRef.close();
  }
}
