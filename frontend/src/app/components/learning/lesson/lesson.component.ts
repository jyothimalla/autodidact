import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { LEARNING_MODULES } from '../learning.data';
import { LearningModule, LearningSubSkill } from '../learning.models';
import { AuthService } from '../../../auth/auth.service';

@Component({
  selector: 'app-lesson',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './lesson.component.html',
  styleUrls: ['./lesson.component.scss']
})
export class LessonComponent {
  module: LearningModule | undefined;
  subskill: LearningSubSkill | undefined;
  safeVideoUrl: SafeResourceUrl | null = null;
  isAdmin = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private sanitizer: DomSanitizer,
    auth: AuthService
  ) {
    this.isAdmin = auth.isAdmin();
    this.route.paramMap.subscribe(params => {
      const moduleId = params.get('moduleId');
      const subskillId = params.get('subskillId');

      this.module = LEARNING_MODULES.find(item => item.id === moduleId);
      this.subskill = this.module?.atoms.find(item => item.id === subskillId);

      if (!this.module || !this.subskill) {
        this.router.navigate(['/learning']);
        return;
      }

      this.safeVideoUrl = this.sanitizer.bypassSecurityTrustResourceUrl(this.subskill.videoUrl);
    });
  }

  startPractice(): void {
    if (!this.module || !this.subskill) return;
    this.router.navigate([`/practice/${this.module.id}`], {
      queryParams: { level: this.subskill.level, subskillId: this.subskill.id }
    });
  }

  startChallenge(): void {
    if (!this.module || !this.subskill) return;
    this.router.navigate([`/challenge/${this.module.id}`], {
      queryParams: { level: this.subskill.level, subskillId: this.subskill.id, mode: 'timed' }
    });
  }
}
