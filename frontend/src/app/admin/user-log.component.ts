import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ConfigService } from '../services/config.service';

@Component({
  selector: 'app-user-log',
  standalone: true,
  templateUrl: './user-log.component.html',
  styleUrls: ['./user-log.component.scss'],
  imports: [FormsModule, CommonModule]
})
export class UserLogComponent implements OnInit {
  logs: any[] = [];
  constructor(private http: HttpClient, private config: ConfigService) {}
  baseUrl = '';
  // baseUrl = environment.apiBaseUrl;
  // baseUrl = appConfig.apiBaseUrl;
  // baseUrl = window.APP_CONFIG.apiBaseUrl;
  ngOnInit(): void {
      this.baseUrl = `${this.config.apiBaseUrl}`;

    this.http.get<any[]>(`${this.baseUrl}/admin/user-logs`).subscribe({
      next: data => this.logs = data,
      error: err => console.error('Error fetching logs', err)
    });
  }
}
