import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../auth/auth.service';
import { environment } from '../../../../environments/environment';
import { ActivatedRoute } from '@angular/router';
import { LeftSidebarComponent } from '../../left-sidebar/left-sidebar.component';
import { RightSidebarComponent } from '../../right-sidebar/right-sidebar.component';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-upload-answers',
  imports: [FormsModule, CommonModule],
  templateUrl: './upload-answers.component.html',
  styleUrl: './upload-answers.component.scss'
})

export class UploadAnswersComponent implements OnInit {
  username = ''; 
  operation = '';
  level = 0;
  sublevel = 'A';
  answerFile: File | null = null;
  uploadStatus = '';
  isDragging = false;
  user_id = 0;

  operations = [
    { value: 'addition', label: 'Addition' },
    { value: 'subtraction', label: 'Subtraction' },
    { value: 'multiplication', label: 'Multiplication' },
    { value: 'division', label: 'Division' },
    { value: 'fmc', label: 'FMC' },
    { value: 'time', label: 'Time' }


  ];

  constructor(private authService: AuthService, private route: ActivatedRoute) {}

  ngOnInit(): void {this.route.queryParams.subscribe(params => {
    this.username = params['username'] || localStorage.getItem('username') || '';
    this.user_id = parseInt(params['user_id'] || localStorage.getItem('user_id') || '0', 10);
  });
  }

  onFileChange(event: any): void {
    this.answerFile = event.target.files[0];
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = false;
    if (event.dataTransfer?.files.length) {
      this.answerFile = event.dataTransfer.files[0];
    }
  }

  onSubmit(): void {
    if (!this.answerFile) {
      this.uploadStatus = '❌ Please select a file.';
      return;
    }

    const formData = new FormData();
    formData.append('file', this.answerFile);
    formData.append('username', this.username);
    formData.append('operation', this.operation);
    formData.append('level', this.level.toString());
    formData.append('sublevel', this.sublevel);

    // call API to upload
    // this.http.post('/upload', formData)...
    this.uploadStatus = '✅ Upload submitted (mock)';
  }
}
