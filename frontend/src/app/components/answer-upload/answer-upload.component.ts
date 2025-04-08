import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { LottieComponent } from 'ngx-lottie';
import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';
import { RightSidebarComponent } from '../right-sidebar/right-sidebar.component';
import { HeaderComponent } from '../header/header.component';
import { FooterComponent } from '../footer/footer.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-answer-upload',
  templateUrl: './answer-upload.component.html',
  styleUrls: ['./answer-upload.component.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule, LeftSidebarComponent, RightSidebarComponent, HeaderComponent, FooterComponent]

})
export class AnswerUploadComponent {
  selectedFile: File | null = null;
  studentName: string = '';
  operation: string = 'addition';
  level: number = 1;
  result: string = '';

  constructor(private http: HttpClient) {}

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  onSubmit(): void {
    if (!this.selectedFile || !this.studentName) {
      alert('Please fill all fields and choose a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);
    formData.append('student_name', this.studentName);
    formData.append('operation', this.operation);
    formData.append('level', this.level.toString());

    this.http.post<any>('http://localhost:8000/upload-answersheet', formData).subscribe({
      next: (response) => {
        this.result = `✅ Score: ${response.score} out of ${response.total}`;
      },
      error: (err) => {
        console.error(err);
        this.result = '❌ Failed to process answer sheet.';
      }
    });
  }
}
