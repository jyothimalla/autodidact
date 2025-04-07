import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class QuizService {

  private apiUrl = 'http://localhost:8000'; // Replace with your FastAPI base URL

  constructor(private http: HttpClient) {}

  getQuestions(operation: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/quiz/questions?operation=${operation}`);
  }

  submitAnswer(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/quiz/answer`, data);
  }

  getResult(sessionId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/quiz/result/${sessionId}`);
  }
}
