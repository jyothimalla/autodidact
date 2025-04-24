import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { QuizService } from '../../services/quiz.service';
import { FormsModule } from '@angular/forms';
import { FooterComponent } from "../footer/footer.component";
import { ConfigService } from '../../services/config.service';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, FormsModule, CommonModule, RouterModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  @Input() username = 'Guest'; // Bind this from parent
  isLoggedIn = false;
  user_id: number = 0;
  awarded_title = '';
  ninjaStars = 0;
  attempts: any[] = [];
  userData: any = null;

  constructor(public router: Router, private route: ActivatedRoute, private config: ConfigService, private http: HttpClient ) {}
  ngOnInit(): void {
    const id = localStorage.getItem('user_id');
    this.user_id = id ? parseInt(id, 10) : 0;
    if (this.user_id > 0) {
      this.loadUserProfile();
    } else {
      this.username = 'Guest';
      this.isLoggedIn = false;
    }
  }
  
  loadUserProfile(): void {
    this.http.get<any>(`${this.config.apiBaseUrl}/user/profile/${this.user_id}`).subscribe({
      next: (res) => {
        this.username = res.username;
        this.awarded_title = res.awarded_title || 'Ninja';
        this.ninjaStars = res.ninja_stars;
        this.attempts = res.progress || [];
        this.isLoggedIn = this.username !== 'Guest';
        console.log('✅ Header user profile loaded:', res);
      },
      error: (err) => {
        console.error('❌ Failed to fetch header user profile:', err);
        this.username = 'Guest';
        this.isLoggedIn = false;
      }
    });
  }
  
  ngDoCheck(): void {
    this.username = this.route.snapshot.queryParams['username']  || localStorage.getItem('username') || 'Guest';
    this.user_id = this.route.snapshot.queryParams['user_id'] || localStorage.getItem('user_id') || '0';

    this.isLoggedIn = this.username !== 'Guest';
  }
  logout(): void {
    localStorage.clear();
    this.username = '';
    this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
      this.router.navigate(['/']);
      alert('Thank you! You have been logged out.');
    });
    this.isLoggedIn = false;
    this.user_id = 0;;
  }
 
  userAccount(): void {
    const userId = localStorage.getItem('user_id');
    if (userId) {
      this.router.navigate(['/user', userId]);
    } else {
      console.error('User ID not found in local storage.');
    }
  }
  goToMyAccount(): void {
    this.user_id = this.route.snapshot.queryParams['user_id'] || localStorage.getItem('user_id') || '0';

    if (this.user_id) {
      console.log('Navigating to /my-account/' + this.user_id);
      this.router.navigate([`/my-account/${this.user_id}`]);
    } else {
      console.error('User ID not found in local storage.');
    }
  }
  
}