import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';



export interface WordProblem {
    question: string;
    answer: string;
  }
  
  @Injectable({ providedIn: 'root' })
  export class WordProblemService {
    private baseUrl = 'http://localhost:8000';
  
    constructor(private http: HttpClient) {}
  
    getWordProblems(userName: string, operation: string, level: number): Observable<WordProblem[]> {
      const url = `${this.baseUrl}/word-problem?user_name=${userName}&operation=${operation}&difficulty=${level}`;
      return this.http.get<WordProblem[]>(url); // Return plain list, not { problems: [...] }
    }
  }
  
