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

@Injectable({ providedIn: 'root' })
export class AuthService {
  private baseUrl = `${environment.apiBaseUrl}/auth`;

  constructor(private http: HttpClient) {}

  register(name: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.baseUrl}/register`, { name, password });
  }

  login(name: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.baseUrl}/login`, { name, password });
  }

  saveUserSession(user_id: number, name: string) {
    localStorage.setItem('user_id', user_id.toString());
    localStorage.setItem('username', name);
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
}