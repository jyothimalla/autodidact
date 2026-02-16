import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { LEARNING_MODULES } from '../learning.data';
import { LearningModule } from '../learning.models';
import { SubskillCardComponent } from '../subskill-card/subskill-card.component';
import { AuthService } from '../../../auth/auth.service';

@Component({
  selector: 'app-module-detail',
  standalone: true,
  imports: [CommonModule, RouterLink, SubskillCardComponent],
  templateUrl: './module-detail.component.html',
  styleUrls: ['./module-detail.component.scss']
})
export class ModuleDetailComponent {
  module: LearningModule | undefined;
  isAdmin = false;

  constructor(private route: ActivatedRoute, private router: Router, auth: AuthService) {
    this.isAdmin = auth.isAdmin();
    this.route.paramMap.subscribe(params => {
      const moduleId = params.get('moduleId');
      this.module = LEARNING_MODULES.find(item => item.id === moduleId);
      if (!this.module) {
        this.router.navigate(['/learning']);
      }
    });
  }
}
