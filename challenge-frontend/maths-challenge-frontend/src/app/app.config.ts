import { ApplicationConfig } from '@angular/core';
import { provideRouter, Routes } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { HomeComponent } from './components/home/home.component';
import { QuizComponent } from './components/quiz/quiz.component';
import { ResultComponent } from './components/result/result.component';
import { LeaderboardComponent } from './components/leaderboard/leaderboard.component';
import { HttpClientModule } from '@angular/common/http';
import { OperationComponent } from './components/operation/operation.component';
import { provideLottieOptions } from 'ngx-lottie';
import player from 'lottie-web';
import { AnimationOptions } from 'ngx-lottie';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'operation', component: OperationComponent },
  { path: 'quiz', component: QuizComponent },
  { path: 'result', component: ResultComponent },
  { path: 'leaderboard', component: LeaderboardComponent },
];
const isBrowser = typeof window !== 'undefined' && typeof document !== 'undefined';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    isBrowser
      ? provideLottieOptions({ player: () => import('lottie-web') })
      : [],
    provideHttpClient(withInterceptors([]))  // ✅ Enable HttpClient here
    
  ]
};
