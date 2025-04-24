import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface UserProgress {
  operation: string;
  level_completed: number;
  dojo_points: number;
  current_level: number;
  total_attempts: number;
}

export interface LevelAttempt {
  level: number;
  operation: string;
  score: number;
  total_questions: number;
  attempt_number: number;
  is_passed: boolean;
  timestamp: string;
}

@Injectable({ providedIn: 'root' })
export class ProgressService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getProgress(user_name: string): Observable<UserProgress[]> {
    return this.http.get<UserProgress[]>(`${this.baseUrl}/progress/view?user_name=${user_name}`);
  }

  getAttempts(user_name: string): Observable<LevelAttempt[]> {
    return this.http.get<LevelAttempt[]>(`${this.baseUrl}/attempts/by-user/${user_name}`);
  }

  getAllAttempts(): Observable<LevelAttempt[]> {
    return this.http.get<LevelAttempt[]>(`${this.baseUrl}/attempts/stats`);
  }
}
export interface LevelAttempt {
  user_name: string;             
  operation: string;
  level: number;
  attempt_number: number;
  score: number;
  total_questions: number;
  is_passed: boolean;
  timestamp: string;
}