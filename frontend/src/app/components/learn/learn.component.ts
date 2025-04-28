import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';

@Component({
  selector: 'app-learn',
  standalone: true,
  imports: [CommonModule, LeftSidebarComponent],
  templateUrl: './learn.component.html',
  styleUrls: ['./learn.component.scss']
})
export class LearnComponent implements OnInit {
  level: number = 0;
  username: string = '';
  user_id: number = 0;
  operation: string = 'addition';
  videoFinished: boolean = false;

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.level = parseInt(params['level'] || '0', 10);
      this.username = params['username'] || 'Guest';
      this.user_id = parseInt(params['user_id'] || '0', 10);
      this.operation = params['operation'] || 'addition';
      console.log(`🎓 Loaded Learn Video for ${this.operation} Level ${this.level}`);
    });
  }

  get videoSrc(): string {
    return `assets/videos/${this.operation}_level${this.level}.mp4`;
  }

  goBack(): void {
    window.history.back();
  }

  onVideoEnd(): void {
    this.videoFinished = true;
    console.log('✅ Video completed for level', this.level);
  }

  tryPractice(): void {
    this.router.navigate(['/practice'], {
      queryParams: {
        level: this.level,
        operation: this.operation,
        username: this.username,
        user_id: this.user_id
      }
    });
  }

  takeChallenge(): void {
    this.router.navigate([`/${this.operation}`], {
      queryParams: {
        level: this.level,
        username: this.username,
        user_id: this.user_id
      }
    });
  }
}
