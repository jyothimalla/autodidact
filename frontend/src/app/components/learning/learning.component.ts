import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { LEARNING_MODULES } from './learning.data';
import { ModuleCardComponent } from './module-card/module-card.component';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-learning',
  standalone: true,
  imports: [CommonModule, ModuleCardComponent],
  templateUrl: './learning.component.html',
  styleUrls: ['./learning.component.scss']
})
export class LearningComponent {
  readonly modules = LEARNING_MODULES;
  isAdmin = false;

  constructor(private auth: AuthService) {
    this.isAdmin = auth.isAdmin();
  }
}
