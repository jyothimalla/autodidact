import { Routes, provideRouter } from '@angular/router';
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { appConfig } from './app.config';
import { HomeComponent } from './components/home/home.component';
import { QuizComponent } from './components/quiz/quiz.component';
import { ResultComponent } from './components/result/result.component';
import { LeaderboardComponent } from './components/leaderboard/leaderboard.component';
import { OperationComponent } from './components/operation/operation.component';
import { LevelComponent } from './components/level/level.component';
import { AdditionComponent } from './components/addition/addition.component';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RightSidebarComponent } from './components/right-sidebar/right-sidebar.component';
import { LeftSidebarComponent } from './components/left-sidebar/left-sidebar.component';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { LottieComponent } from 'ngx-lottie';
import { SubtractionComponent } from './components/subtraction/subtraction.component';
import { MultiplicationComponent } from './components/multiplication/multiplication.component';
import { SudokuComponent } from './components/sudoku/sudoku.component';
import { DivisionComponent } from './components/division/division.component';
import { AnswerUploadComponent } from './components/answer-upload/answer-upload.component';
import { FMCComponent } from './components/fmc/fmc.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { ProgressComponent } from './progress/progress.component';
import { AdminDashboardComponent } from './admin/admin-dashboard.component';
import { authGuard } from './auth/auth.guard';
import { AuthService } from './auth/auth.service';
import { TestAdditionComponent } from './components/test-addition/test-addition.component';
import { MyAccountComponent } from './components/my-account/my-account.component';
import { LearnComponent } from './components/learn/learn.component';
import { PracticeComponent } from './components/practice/practice.component';

export const routes: Routes = [
  { path: 'login', loadComponent: () => import('./auth/login/login.component').then(m => m.LoginComponent) },
  { path: 'register', loadComponent: () => import('./auth/register/register.component').then(m => m.RegisterComponent) },
  { path: '', component: HomeComponent },
  {path: 'header', loadComponent: () => import('./components/header/header.component').then(m => m.HeaderComponent)},
  
  { path: 'level', component: LevelComponent },
  { path: 'quiz', component: QuizComponent },
  { path: 'result', component: ResultComponent },
  { path:'leaderboard', component: LeaderboardComponent },
  { path: 'addition', loadComponent: () => import('./components/addition/addition.component').then(m => m.AdditionComponent) },
  {path: 'subtraction', loadComponent: () => import('./components/subtraction/subtraction.component').then(m => m.SubtractionComponent)},
  {path: 'multiplication', loadComponent: () => import('./components/multiplication/multiplication.component').then(m => m.MultiplicationComponent)},
  {path: 'division', loadComponent: () => import('./components/division/division.component').then(m => m.DivisionComponent)},
  {path: 'fmc', loadComponent: () => import('./components/fmc/fmc.component').then(m => m.FMCComponent)},
  {path: 'left_sidebar', component: LeftSidebarComponent},
  {path: 'footer', component: FooterComponent},
  {path: 'lottie', component: LottieComponent},
  {path: 'sudoku', component: SudokuComponent},
  {path: 'right_sidebar', component: RightSidebarComponent},
  {path: 'upload-answers', component: AnswerUploadComponent },
  { path: 'progress', loadComponent: () => import('./progress/progress.component').then(m => m.ProgressComponent), 
    canActivate: [authGuard]},
  {path: 'operation', loadComponent: () => import('./components/operation/operation.component').then(m => m.OperationComponent) },
  { path: 'operation/:type',  loadComponent: () => import('./components/operation/operation.component').then(m => m.OperationComponent) },
  { path: 'operation/:type/:level', loadComponent: () => import('./components/quiz/quiz.component').then(m => m.QuizComponent) },
  { path: 'learn/:operation', loadComponent: () => import('./components/learn/learn.component').then(m => m.LearnComponent)},
  { path: 'learn/:type', loadComponent: () => import('./components/learn/learn.component').then(m => m.LearnComponent) },
  { path: 'practice/:type', loadComponent: () => import('./components/practice/practice.component').then(m => m.PracticeComponent) },
  { path: 'challenge/:type', loadComponent: () => import('./components/quiz/quiz.component').then(m => m.QuizComponent) },

  {path: 'practice/:operation', loadComponent: () => import('./components/practice/practice.component').then(m => m.PracticeComponent)},
   {path: 'my-account/:id',
    loadComponent: () => import('./components/my-account/my-account.component').then(m => m.MyAccountComponent)
  },
    {path: 'admin', loadComponent: () => import('./admin/admin-dashboard.component').then(m => m.AdminDashboardComponent),
    canActivate: [authGuard]
  },

  {
    path: 'test-addition',
    loadComponent: () => import('./components/test-addition/test-addition.component').then(m => m.TestAdditionComponent),
  },
];
