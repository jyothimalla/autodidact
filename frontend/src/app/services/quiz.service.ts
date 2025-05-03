// src/app/services/quiz.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
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
  constructor(
    private http: HttpClient,
    private config: ConfigService
  ) {}

  private get apiBaseUrl(): string {
    return environment.apiBaseUrl || this.config.apiBaseUrl;
  }

  // ✅ Start a quiz session
  startSession(operation: string, level: number): Observable<any> {
    const user_id = localStorage.getItem('user_id');
    const username = localStorage.getItem('username') || 'Guest';
    if (!user_id) {
      throw new Error('User not logged in. Cannot start session.');
    }

    return this.http.post(`${this.apiBaseUrl}/start-session`, {
      user_id: parseInt(user_id),
      username,
      operation,
      level
    });
  }

  // ✅ Centralized question fetcher based on operation and mode
  getQuestionsByOperation(
    operation: string,
    level: number,
    mode: 'practice' | 'challenge' | 'guest' = 'practice'
  ): Observable<any[]> {
    const endpointMap: { [key: string]: string } = {
      addition: 'addition/questions',
      subtraction: 'subtraction/questions',
      multiplication: 'multiplication/questions',
      division: 'division/questions',
      fmc: 'fmc/questions',
    };

    const endpoint = endpointMap[operation] || endpointMap['addition'];
    let limit = mode === 'challenge' ? 10 : 5;

    const params = new HttpParams()
      .set('level', level.toString())
      .set('limit', limit.toString());

    return this.http.get<any[]>(`${this.apiBaseUrl}/${endpoint}`, { params });
  }

  // ✅ Submit challenge score
  submitChallengeAttempt(data: {
    user_id: number;
    operation: string;
    level: number;
    score: number;
    total_questions: number;
  }): Observable<SubmitChallengeResponse> {
    const params = new HttpParams()
      .set('user_id', data.user_id.toString())
      .set('operation', data.operation)
      .set('level', data.level.toString())
      .set('score', data.score.toString())
      .set('total_questions', data.total_questions.toString());

    return this.http
      .post<SubmitChallengeResponse>(`${this.apiBaseUrl}/level-attempt/`, {}, { params })
      .pipe(retry(3));
  }

  // ✅ Submit a regular result (optional, not used for challenge mode)
  submitResult(data: any): Observable<any> {
    return this.http.post(`${this.apiBaseUrl}/quiz/submit-result`, data);
  }

  // ✅ Save user progress
  saveProgress(data: any): Observable<any> {
    return this.http.post(`${this.apiBaseUrl}/save-progress`, data);
  }

  // ✅ Get user-specific questions from stored session
  getSessionQuestions(): Observable<any[]> {
    const user_id = localStorage.getItem('user_id');
    const operation = localStorage.getItem('operation');
    return this.http.get<any[]>(
      `${this.apiBaseUrl}/quiz/questions?user_id=${user_id}&operation=${operation}`
    );
  }

  // ✅ Get full progress
  getUserProgress(): Observable<any> {
    const user_id = localStorage.getItem('user_id');
    return this.http.get<any>(`${this.apiBaseUrl}/progress/${user_id}`);
  }

  // ✅ Get progress filtered by operation
  getUserProgressByOperation(operation: string): Observable<any> {
    const user_id = localStorage.getItem('user_id');
    return this.http.get<any>(`${this.apiBaseUrl}/progress/${user_id}?operation=${operation}`);
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

  getPracticeQuestions(level: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiBaseUrl}/practice-questions?level=${level}`);
  }

  getQuestions(username: string): Observable<any[]> {
    const user_id = localStorage.getItem('user_id');
    const operation = localStorage.getItem('operation');
    const level = localStorage.getItem('level');
    return this.http.get<any[]>(`${this.apiBaseUrl}/quiz/questions?user_id=${user_id}&operation=${operation}&level=${level}`);
  }
 
}