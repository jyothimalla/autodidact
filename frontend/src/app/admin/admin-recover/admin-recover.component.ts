import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-admin-recover',
  standalone: true,
  templateUrl: './admin-recover.component.html',
  styleUrls: ['./admin-recover.component.scss'],
  imports: [FormsModule, CommonModule],
})
export class AdminRecoverComponent implements OnInit {
  inactiveUsers: any[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadInactiveUsers();
  }

  loadInactiveUsers(): void {
    this.http.get<any[]>('http://localhost:8000/admin/inactive-users')
      .subscribe({
        next: data => this.inactiveUsers = data,
        error: err => console.error('❌ Failed to load users:', err)
      });
  }

  reactivateUser(userId: number): void {
    this.http.post(`http://localhost:8000/admin/reactivate-user/${userId}`, {})
      .subscribe({
        next: () => {
          alert('✅ User reactivated');
          this.loadInactiveUsers();
        },
        error: err => console.error('❌ Failed to reactivate user:', err)
      });
  }
}
