import { Component, OnInit, Input, OnDestroy, HostListener, ElementRef } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { QuizService } from '../../services/quiz.service';
import { FormsModule } from '@angular/forms';
import { FooterComponent } from "../footer/footer.component";
import { ConfigService } from '../../services/config.service';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { UserService } from '../../services/user.service';
import { NavigationEnd } from '@angular/router';
import { Subscription } from 'rxjs';

interface UserProfile {
  username: string;
  awarded_title?: string;
  ninja_stars?: number;
  progress?: any[];
  user_id: 0;
}


@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})

export class HeaderComponent implements OnInit, OnDestroy {
  @Input() username = 'Guest'; // Bind this from parent
  isLoggedIn = false;
  user_id: number = 0;
  awarded_title = '';
  ninjaStars = 0;
  attempts: any[] = [];
  userData: any = null;
  dropdownOpen = false;
  private routerSub?: Subscription;


  constructor(public router: Router,
              private route: ActivatedRoute,
              private config: ConfigService,
              private userService: UserService,
              private http: HttpClient,
              private quizService: QuizService,
              private elRef: ElementRef) {}

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent): void {
    if (!this.elRef.nativeElement.contains(event.target)) {
      this.dropdownOpen = false;
    }
  }

  toggleDropdown(event: MouseEvent): void {
    event.stopPropagation();
    this.dropdownOpen = !this.dropdownOpen;
  }

  closeDropdown(): void {
    this.dropdownOpen = false;
  }
  
  ngOnInit(): void {
    this.refreshUserState();
    this.routerSub = this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.refreshUserState();
      }
    });
  }

  ngOnDestroy(): void {
    this.routerSub?.unsubscribe();
  }

  private refreshUserState(): void {
    // Prefer the persisted session user. Query params are only a fallback.
    const routeUsername = this.route.snapshot.queryParams['username'];
    const routeUserId = this.route.snapshot.queryParams['user_id'];
    this.username = localStorage.getItem('username') || routeUsername || 'Guest';
    this.user_id = parseInt(localStorage.getItem('user_id') || routeUserId || '0', 10);
    this.isLoggedIn = this.username !== 'Guest' && this.user_id > 0;

    if (!this.isLoggedIn) {
      this.attempts = [];
      return;
    }

    this.quizService.getUserProgress(this.user_id).subscribe({
      next: (res) => {
        this.attempts = res.attempts || [];
      },
      error: () => {
        this.attempts = [];
      }
    });
  }
  goToMyAccount(): void {
    this.router.navigate(['/my-account']);
  }

  logout(): void {
    this.closeDropdown();
    localStorage.clear();
    this.router.navigate(['/']);
  }
  userAccount() {
    this.closeDropdown();
    const userId = localStorage.getItem('user_id');
    if (userId) {
      this.router.navigate(['/my-account', userId]);
    } else {
      console.error('User ID not found in local storage.');
    }
  }
 
  goToLearning(): void {
    this.router.navigate(['/learning']);
  }

  goToPractice(): void {
    this.router.navigate(['/practice']);
  }

  goToTest(): void {
    this.router.navigate(['/mock-test']);
  }

  goToDashboard(): void {
    this.router.navigate(['/my-account']);
  }

  goToAnalytics(): void {
    this.closeDropdown();
    this.router.navigate(['/analytics']);
  }
  
}
