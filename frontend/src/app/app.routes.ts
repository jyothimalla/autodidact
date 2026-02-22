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
import { FMCComponent } from './components/fmc/fmc.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { ProgressComponent } from './progress/progress.component';
import { AdminDashboardComponent } from './admin/admin-dashboard/admin-dashboard.component';
import { authGuard } from './auth/auth.guard';
import { AuthService } from './auth/auth.service';
import { TestAdditionComponent } from './components/test-addition/test-addition.component';
import { MyAccountComponent } from './components/my-account/my-account.component';
import { LearnComponent } from './components/learn/learn.component';
import { PracticeComponent } from './components/practice/practice.component';
import { AnalyticsComponent } from './components/analytics/analytics.component';
import { TimeQuestionsComponent } from './components/time-questions/time-questions.component';
import { UploadAnswersComponent } from './components/analytics/upload-answers/upload-answers.component';
import { AdminRecoverComponent } from './admin/admin-recover/admin-recover.component';
import { PaperDownloadComponent } from './components/paper-download/paper-download.component';
import { QuizService } from './services/quiz.service';
import { UserLogComponent } from './admin/user-log.component';

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
  {path: 'time-questions', loadComponent: () => import('./components/time-questions/time-questions.component').then(m => m.TimeQuestionsComponent)},
  {path: 'left_sidebar', component: LeftSidebarComponent},
  {path: 'footer', component: FooterComponent},
  {path: 'lottie', component: LottieComponent},
  {path: 'sudoku', component: SudokuComponent},
  {path: 'right_sidebar', component: RightSidebarComponent},
  {path: 'upload-answers', component: UploadAnswersComponent},
  { path: 'progress', loadComponent: () => import('./progress/progress.component').then(m => m.ProgressComponent), 
    canActivate: [authGuard]},
  {path: 'operation', loadComponent: () => import('./components/operation/operation.component').then(m => m.OperationComponent) },
  { path: 'operation/:type',  loadComponent: () => import('./components/operation/operation.component').then(m => m.OperationComponent) },
  { path: 'operation/:type/:level', loadComponent: () => import('./components/quiz/quiz.component').then(m => m.QuizComponent) },
  { path: 'learning', loadComponent: () => import('./components/learning/learning.component').then(m => m.LearningComponent) },
  { path: 'learning/:moduleId/:topicId/level/:level', loadComponent: () => import('./components/learning/lesson/lesson.component').then(m => m.LessonComponent) },
  { path: 'learning/:moduleId/:subskillId', loadComponent: () => import('./components/learning/lesson/lesson.component').then(m => m.LessonComponent) },
  { path: 'learning/:moduleId', loadComponent: () => import('./components/learning/module-detail/module-detail.component').then(m => m.ModuleDetailComponent) },
  { path: 'learn/:operation', loadComponent: () => import('./components/learn/learn.component').then(m => m.LearnComponent)},
  { path: 'learn/:type', loadComponent: () => import('./components/learn/learn.component').then(m => m.LearnComponent) },
  { path: 'practice', loadComponent: () => import('./components/practice/practice.component').then(m => m.PracticeComponent) },
  { path: 'practice/:type', loadComponent: () => import('./components/practice/practice.component').then(m => m.PracticeComponent) },
  { path: 'challenge/:type', loadComponent: () => import('./components/quiz/quiz.component').then(m => m.QuizComponent) },

  {path: 'practice/:operation', loadComponent: () => import('./components/practice/practice.component').then(m => m.PracticeComponent)},
   {path: 'my-account/:id',
    loadComponent: () => import('./components/my-account/my-account.component').then(m => m.MyAccountComponent)
  },
    {path: 'admin', loadComponent: () => import('./admin/admin-dashboard/admin-dashboard.component').then(m => m.AdminDashboardComponent),
    canActivate: [authGuard]
  },
  {
  path: 'admin/recover',
  loadComponent: () => import('./admin/admin-recover/admin-recover.component').then(m => m.AdminRecoverComponent)
},
{path: 'admin-login', loadComponent: () => import('./admin/admin-login/admin-login.component').then(m => m.AdminLoginComponent)},
{path: 'admin-recover', loadComponent: () => import('./admin/admin-recover/admin-recover.component').then(m => m.AdminRecoverComponent)},
{path: 'user-log', component: UserLogComponent},

  {path: 'analytics', loadComponent:() => import('./components/analytics/analytics.component').then(m=>m.AnalyticsComponent)},
  { path: 'parent-paper', loadComponent: () => import('./components/parent-paper/parent-paper.component').then(m => m.ParentPaperComponent), canActivate: [authGuard] },
  { path: 'mock-test', loadComponent: () => import('./components/mock-test/mock-test.component').then(m => m.MockTestComponent), canActivate: [authGuard] },
  { path: 'test/:testId/submit', loadComponent: () => import('./components/mock-test/mock-test.component').then(m => m.MockTestComponent) },
  { path: 'practice-submit/:attemptId', loadComponent: () => import('./components/practice-submit/practice-submit.component').then(m => m.PracticeSubmitComponent) }
];
