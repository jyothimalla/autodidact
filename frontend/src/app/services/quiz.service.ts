// src/app/services/quiz.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import { ConfigService } from '../services/config.service'; 
import { retry } from 'rxjs/operators';
import { environment } from '../../environments/environment';

interface SubmitChallengeResponse {
  message: string;
  level_attempt_id: number;
  attempt_number: number;
  is_passed: boolean;
}

@Injectable({ providedIn: 'root' })

export class QuizService {
  username: string = '';
  
  constructor(
  private router: Router,
  private http: HttpClient,  
  private config: ConfigService) {}
  
  private get apiBaseUrl(): string {
    return environment.apiBaseUrl || this.config.apiBaseUrl;

  }
  startSession(operation: string, level: number): Observable<any> {
    const user_id = localStorage.getItem('user_id');
    const username = localStorage.getItem('username') || 'Guest';
    if (!user_id) {
      throw new Error('User not logged in. Cannot start session.');
    }

    return this.http.post(`${this.apiBaseUrl}/start-session`, {
      user_id: parseInt(user_id),
      username: username,
      operation,
      level
    });
  }

  getAdditionQuestions(level: number): Observable<any[]> {
  console.log(`🔍 Sending GET to: /addition/questions?level=${level}`);
  return this.http.get<any[]>(`${this.apiBaseUrl}/addition/questions?level=${level}`);
  }
  getAdditionPracticeQuestions(level: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiBaseUrl}/addition/practice-questions?level=${level}`);
  }
  getSubtractionQuestions(level: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiBaseUrl}/subtraction/questions?level=${level}`);
  }
  getDivisionQuestions(level: number): Observable<any[]> {
  return this.http.get<any[]>(`${this.apiBaseUrl}/division/questions?level=${level}`);
  }
  getMultiplicationQuestions(level: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiBaseUrl}/multiplication/questions?level=${level}`);
  }
  getFMCQuestions(level: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiBaseUrl}/fmc/questions?level=${level}`);
  }

  getQuestions(username: string): Observable<any[]> {
    const user_id = localStorage.getItem('user_id');
    const operation = localStorage.getItem('operation');
    const level = localStorage.getItem('level');
    return this.http.get<any[]>(`${this.apiBaseUrl}/quiz/questions?user_id=${user_id}&operation=${operation}&level=${level}`);
  }
  submitResult(data: any): Observable<any> {
    return this.http.post(`${this.apiBaseUrl}/quiz/submit-result`, data);
  }
  saveProgress(data: any): Observable<any> {
    return this.http.post(`${this.apiBaseUrl}/save-progress`, data);
  }

  getSessionQuestions(): Observable<any[]> {
    const user_id = localStorage.getItem('user_id');
    const operation = localStorage.getItem('operation');
    return this.http.get<any[]>(`${this.apiBaseUrl}/quiz/questions?user_id=${user_id}&operation=${operation}`);
  }
 
  getUserProgress(): Observable<any> {
    const user_id = localStorage.getItem('user_id');
    return this.http.get<any>(`${this.apiBaseUrl}/progress/${user_id}`);
  }
  getUserProgressByOperation(operation: string): Observable<any> {
    const user_id = localStorage.getItem('user_id');
    return this.http.get<any>(`${this.apiBaseUrl}/progress/${user_id}?operation=${operation}`);
  }

  submitChallengeAttempt(data: {user_id: number, operation: string, level: number, score: number, total_questions: number}) {

    const params = new URLSearchParams({
      user_id: data.user_id.toString(),
      operation: data.operation,
      level: data.level.toString(),
      score: data.score.toString(),
      total_questions: data.total_questions.toString()
    }).toString();
    console.log('Saving challenge answers:', data);

    return this.http.post<SubmitChallengeResponse>(`${this.apiBaseUrl}/level-attempt/?${params}`, {})
      .pipe(retry(3)    );}
  }
