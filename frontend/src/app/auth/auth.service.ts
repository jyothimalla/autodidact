// ✅ src/app/auth/auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// auth.service.ts
import { environment } from '../../environments/environment';


interface AuthResponse {
  message: string;
  user_id: number;
  name?: string;
}

interface CurrentUser {
  id: number | null;
  name: string | null;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private baseUrl = `${environment.apiBaseUrl}/auth`;

  constructor(private http: HttpClient) {}

  register(username: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.baseUrl}/register`, { username, password });
  }
  isAdmin(): boolean {
    return localStorage.getItem('role') === 'admin';
  }

  login(username: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.baseUrl}/login`, { username, password });
  }

  saveUserSession(user_id: number, username: string) {
    localStorage.setItem('user_id', user_id.toString());
    localStorage.setItem('username', username);
  }

  logout() {
    localStorage.clear();
  }

  getUsername(): string | null {
    return localStorage.getItem('username');
  }

  getUserId(): number | null {
    const id = localStorage.getItem('user_id');
    return id ? parseInt(id) : null;
  }

  getCurrentUser(): CurrentUser {
    return {
      id: this.getUserId(),
      name: this.getUsername(),
    };
  }
}
