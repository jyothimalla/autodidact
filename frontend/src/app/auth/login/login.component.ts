import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { EventEmitter, Output, Optional } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { appConfig } from '../../app.config';
import { routes } from '../../app.routes';
import { ActivatedRoute } from '@angular/router';
import { ConfigService } from '../../services/config.service';

declare global {
  interface Window {
    APP_CONFIG: any;
  }
}

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
  baseUrl: string = '';
  loginError: string = '';
  

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router,
    private route: ActivatedRoute,
    private config: ConfigService,

    @Optional() public dialogRef: MatDialogRef<LoginComponent>
  ) 
  {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
    

    // ✅ Set baseUrl at runtime inside constructor
    const isLocal =
      window.location.hostname === 'localhost' ||
      window.location.hostname === '127.0.0.1';
    const defaultApiBase = isLocal ? 'http://localhost:8000' : 'https://api.autodidact.uk';
    const runtimeApiBase =
      this.config.apiBaseUrl ||
      window.APP_CONFIG?.apiBaseUrl ||
      environment.apiBaseUrl ||
      defaultApiBase;

    this.baseUrl = `${runtimeApiBase.replace(/\/+$/, '')}/auth/login`;
  }

  onSubmit(): void {
    if (this.loginForm.invalid) return;

    const { username, password } = this.loginForm.value;
    console.log('🔍 Loaded baseUrl:', this.baseUrl);
    console.log('📦 APP_CONFIG:', window.APP_CONFIG);
    
    this.http.post<any> (this.baseUrl, {
      username, password
    }).subscribe({
      next: (res) => {
        localStorage.setItem('username', res.username);
        localStorage.setItem('user_id', res.user_id.toString());
        if (res.is_admin) {
          localStorage.setItem('role', 'admin');
        } else {
          localStorage.removeItem('role');
        }
        alert(`✅ Welcome, ${res.username} (ID: ${res.user_id})!`);

        this.dialogRef?.close();
        this.router.navigate(['/learning'], {
          queryParams: {username: res.username, user_id: res.user_id }
        });
      },
      error: (err) => {
    if (err.status === 403) {
      this.loginError = '⚠️ Your account is deactivated. Please contact support.';
    } else {
      this.loginError = '❌ Invalid credentials.';
    }
  }
    });
  }
}
