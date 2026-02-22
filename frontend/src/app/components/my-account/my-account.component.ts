import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ConfigService } from '../../services/config.service';
import { environment } from '../../../environments/environment';
import { AuthService } from '../../auth/auth.service';
import { Router } from '@angular/router';
import { Injectable } from '@angular/core';
import { HttpHeaders } from '@angular/common/http';
import { QuizService } from '../../services/quiz.service';

@Component({
  selector: 'app-my-account',
  templateUrl: './my-account.component.html',
  styleUrls: ['./my-account.component.scss'],
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
})
export class MyAccountComponent implements OnInit {
  private readonly studentYearStorageKey = 'student_year';
  private readonly analyticsYearStorageKey = 'analytics_year_level';
  user_id: number = 0;
  username: string = '';
  awardedName: string = '';
  ninjaStars: number = 0;
  studentYear: number = 4;
  attempts: any[] = [];
  isEditing: boolean = false;
  baseUrl = environment.apiBaseUrl;

  // Fields for editing
  editUsername: string = '';
  editEmail: string = '';
  editPassword: string = '';
  editConfirmPassword: string = '';

  constructor(private route: ActivatedRoute, private http: HttpClient,
      private config: ConfigService , private router: Router,
      private quizService: QuizService) {}

      ngOnInit(): void {
        this.initializeStudentYear();
        const idParam = this.route.snapshot.paramMap.get('id');
        this.user_id = idParam ? parseInt(idParam, 10) : 0;
        this.username = localStorage.getItem('username') || '';
      
        this.loadUserProfile();
      
        // ✅ Pass user_id to the service method
        this.quizService.getUserProgress(this.user_id).subscribe({
          next: (res) => {
            this.ninjaStars = res.ninja_stars;
            this.attempts = res.attempts;
          },
          error: (err) => {
            console.error('❌ Failed to load progress:', err);
          }
        });
      }

  private initializeStudentYear(): void {
    const saved = Number(localStorage.getItem(this.studentYearStorageKey));
    this.studentYear = saved >= 1 && saved <= 13 ? saved : 4;
    localStorage.setItem(this.studentYearStorageKey, String(this.studentYear));
    localStorage.setItem(this.analyticsYearStorageKey, String(this.studentYear));
  }

  onStudentYearChange(event: Event): void {
    const nextYear = Number((event.target as HTMLSelectElement).value);
    if (nextYear < 1 || nextYear > 13) {
      return;
    }
    this.studentYear = nextYear;
    localStorage.setItem(this.studentYearStorageKey, String(nextYear));
    localStorage.setItem(this.analyticsYearStorageKey, String(nextYear));
  }
      
  loadUserProfile(): void {
    console.log('🔍 Fetching user profile for ID:', this.user_id);
    this.http.get<any>(`${this.config.apiBaseUrl}/user/profile/${this.user_id}`).subscribe({
      next: (res) => {
        this.username = res.username;
        this.awardedName = res.awarded_title;
        this.ninjaStars = res.ninja_stars;
        this.attempts = res.progress || [];
        const yearFromProfile = Number(String(res.year || '').replace(/[^\d]/g, ''));
        if (yearFromProfile >= 1 && yearFromProfile <= 13) {
          this.studentYear = yearFromProfile;
          localStorage.setItem(this.studentYearStorageKey, String(yearFromProfile));
          localStorage.setItem(this.analyticsYearStorageKey, String(yearFromProfile));
        }
        console.log('✅ User profile loaded:', res);
      },
      error: (err) => {
        console.error('❌ Failed to fetch user profile:', err);
      }
    });
  }

  getStarsForLevel(level: number): string {
    const progress = this.attempts.find((a: any) => a.level === level);
    return progress ? '★'.repeat(progress.dojo_points || 0) : '☆';
  }

  // 🔧 Trigger edit mode
  editProfile(): void {
    this.isEditing = true;
  }

  // ✅ Save edits to backend
  saveChanges(): void {
    const updatedData = {
      username: this.editUsername,
      email: this.editEmail,
      password: this.editPassword,
    };

    this.http.put(`${this.baseUrl}/user/update/${this.user_id}`, updatedData).subscribe({
      next: () => {
        alert('✅ Profile updated successfully!');
        this.username = this.editUsername;
        this.isEditing = false;
      },
      error: (err) => {
        console.error('❌ Update failed:', err);
        alert('Failed to update profile.');
      }
    });
  }

  cancelEdit(): void {
    this.isEditing = false;
    this.editUsername = this.username;
  }
  // 🔒 Check if user is logged in
  isLoggedIn(): boolean {
    return !!localStorage.getItem('user_id');
  }
  deleteAccount(): void {
    if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      this.http.delete(`${this.baseUrl}/user/delete/${this.user_id}`).subscribe({
        next: () => {
          alert('✅ Account deleted successfully!');
          localStorage.removeItem('user_id');
          localStorage.removeItem('username');
          window.location.href = '/';
        },
        error: (err) => {
          console.error('❌ Failed to delete account:', err);
          alert('Failed to delete account.');
        }
      });
    }
  }
  // 🔑 Check if user is a guest
  isGuest(): boolean {
    return this.username === 'Guest';
  }
  goToOperations(): void {
    this.router.navigate(['/operation'], {
      queryParams: {
        username: this.username,
        user_id: this.user_id
      }
    });
  }
deactivateAccount(): void {
  if (confirm('Are you sure you want to deactivate your account? You can reactivate it later by contacting support.')) {
    this.http.delete(`${this.baseUrl}/user/delete/${this.user_id}`).subscribe({
      next: () => {
        alert('✅ Account deactivated successfully!');
        localStorage.removeItem('user_id');
        localStorage.removeItem('username');
        window.location.href = '/';
      },
      error: (err) => {
        console.error('❌ Failed to deactivate account:', err);
        alert('Failed to deactivate account.');
      }
    });
  }
}
  
}
