import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.scss'],
  standalone: true,
  imports: [CommonModule]
})
export class UserProfileComponent implements OnInit {
  userId = '';
  userProfile: any = null;
  isLoading = true;

  constructor(private route: ActivatedRoute, private http: HttpClient) {}

  ngOnInit(): void {
    this.userId = this.route.snapshot.paramMap.get('id') || localStorage.getItem('user_id') || '';
    this.fetchUserProfile();
  }

  fetchUserProfile() {
    this.http.get(`http://localhost:8000/user/profile/${this.userId}`).subscribe({
      next: (res: any) => {
        this.userProfile = res;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('❌ Failed to load profile:', err);
        this.isLoading = false;
      }
    });
  }
}
