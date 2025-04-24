// src/app/test-addition.component.ts
import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-test-addition',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './test-addition.component.html',
  styleUrls: ['./test-addition.component.scss']
})
export class TestAdditionComponent implements OnInit {
  questions: any[] = [];
  error = '';
  
  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    console.log("🚀 TestAdditionComponent loaded");
  }
  
  load() {
    const level = 0;
    const url = `http://localhost:8000/addition/questions?level=${level}`;
  
    this.http.get<any[]>(url).subscribe({
      next: (data) => {
        console.log('✅ Got questions:', data);
        this.questions = data;
      },
      error: (err) => {
        console.error('❌ Error:', err);
        this.error = 'Failed to load questions';
      }
    });
  }
}
