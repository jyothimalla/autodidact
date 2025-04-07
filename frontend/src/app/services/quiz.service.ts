// src/app/services/quiz.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import { ConfigService } from '../services/config.service'; 


@Injectable({ providedIn: 'root' })

export class QuizService {
  private baseUrl = 'http://localhost:8000'; // FastAPI backend

  constructor(
    private router: Router,
    private http: HttpClient,  private config: ConfigService) {}
  
  startSession(name: string, operation: string, level: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/start-session`, { name, operation, level });
  }
    
  getQuestions(name: string): Observable<any> {
    const operation = localStorage.getItem('operation') || 'multiplication';
    return this.http.get(`${this.baseUrl}/quiz/questions?name=${name}&operation=${operation}`);
  }
  getAdditionQuestions(level: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/addition/questions?level=${level}`);
  }
  getSubtractionQuestions(level: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/subtraction/questions?level=${level}`);
  }
  getDivisionQuestions(level: number): Observable<any[]> {
  return this.http.get<any[]>(`${this.baseUrl}/division/questions?level=${level}`);
}

getMultiplicationQuestions(level: number): Observable<any[]> {
  return this.http.get<any[]>(`${this.baseUrl}/multiplication/questions?level=${level}`);
}

  submitResult(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/quiz/submit-result`, data);
  }
}
