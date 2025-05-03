import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { QuizService } from '../../services/quiz.service';
import { FormsModule } from '@angular/forms';
import { FooterComponent } from "../footer/footer.component";
import { ConfigService } from '../../services/config.service';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { UserService } from '../../services/user.service';


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
  
  
  constructor(public router: Router, 
              private route: ActivatedRoute, 
              private config: ConfigService, 
              private userService: UserService,
              private http: HttpClient ) {}
  
  ngOnInit(): void {
    this.username = this.route.snapshot.queryParams['username']  || localStorage.getItem('username') || 'Guest';
    this.user_id = this.route.snapshot.queryParams['user_id'] || localStorage.getItem('user_id') || '0';

    this.isLoggedIn = this.username !== 'Guest';
  }
  
 
  
}