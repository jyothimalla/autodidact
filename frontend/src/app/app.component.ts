import { Component } from '@angular/core';
import { RouterModule, Router, ActivatedRoute } from '@angular/router';
import { HeaderComponent } from './components/header/header.component';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FooterComponent } from './components/footer/footer.component';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatIconModule } from '@angular/material/icon';
import {routes } from './app.routes';
import { provideRouter, withHashLocation } from '@angular/router';
import { appConfig } from './app.config';
import { provideHttpClient } from '@angular/common/http';
import { ConfigService } from './services/config.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule, FormsModule, HeaderComponent, CommonModule, FooterComponent, MatSlideToggleModule ], 
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent {
  provider = [provideRouter(routes, withHashLocation()), provideHttpClient(), ConfigService];
  username = localStorage.getItem('username') || 'Guest'; // <-- reads from localStorage

  constructor(public router: Router,   
              private config: ConfigService,  
              private http: HttpClient) 
  { console.log('AppComponent initialized 🚀');
    
  } 
  
  title = 'Autididact - Kids Self Learning Platform';
  
  
}
