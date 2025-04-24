

import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter, Routes } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { routes } from './app.routes';
import { HomeComponent } from './components/home/home.component';
import { QuizComponent } from './components/quiz/quiz.component';
import { ResultComponent } from './components/result/result.component';
import { LeaderboardComponent } from './components/leaderboard/leaderboard.component';
import { OperationComponent } from './components/operation/operation.component';
import { FooterComponent } from './components/footer/footer.component';
import { HeaderComponent } from './components/header/header.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { AdditionComponent } from './components/addition/addition.component';
import { FormsModule } from '@angular/forms'; 
import { MatSlideToggleModule } from '@angular/material/slide-toggle';  // ✅ Add this
import { provideLottieOptions } from 'ngx-lottie';
import player from 'lottie-web';


const isBrowser = typeof window !== 'undefined' && typeof document !== 'undefined';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([])),
    importProvidersFrom(FormsModule),             // ✅ Fix ngModel
    importProvidersFrom(MatSlideToggleModule),    // ✅ Fix slide toggle
    ...(isBrowser ? [provideLottieOptions({ player: () => import('lottie-web') })] : [])
  ]
};
