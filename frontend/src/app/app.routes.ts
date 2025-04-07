import { Routes } from '@angular/router';
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


export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'operation', component: OperationComponent },
  { path: 'level', component: LevelComponent },
  { path: 'quiz', component: QuizComponent },
  { path: 'result', component: ResultComponent },
  { path:'leaderboard', component: LeaderboardComponent },
  { path: 'addition', loadComponent: () => import('./components/addition/addition.component').then(m => m.AdditionComponent) },
  {path: 'subtraction', loadComponent: () => import('./components/subtraction/subtraction.component').then(m => m.SubtractionComponent)},
  {path: 'multiplication', loadComponent: () => import('./components/multiplication/multiplication.component').then(m => m.MultiplicationComponent)},
  {path: 'division', loadComponent: () => import('./components/division/division.component').then(m => m.DivisionComponent)},
  {path: 'left_sidebar', component: LeftSidebarComponent},
  {path: 'header', component: HeaderComponent},
  {path: 'footer', component: FooterComponent},
  {path: 'lottie', component: LottieComponent},
  {path: 'sudoku', component: SudokuComponent},
  {path: 'right_sidebar', component: RightSidebarComponent}
];
