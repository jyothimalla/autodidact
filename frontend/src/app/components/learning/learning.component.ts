import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { SUBJECTS } from './learning-subjects.data';
import { AuthService } from '../../auth/auth.service';
import { Subject, LearningModule, LearningTopic, LearningAtom } from './learning.models';

@Component({
  selector: 'app-learning',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './learning.component.html',
  styleUrls: ['./learning.component.scss']
})
export class LearningComponent {
  readonly subjects = SUBJECTS;
  isAdmin = false;

  // Navigation state
  selectedSubject: Subject | null = null;
  selectedModule: LearningModule | null = null;
  selectedTopic: LearningTopic | null = null;

  constructor(
    private auth: AuthService,
    private router: Router
  ) {
    this.isAdmin = auth.isAdmin();
  }

  selectSubject(subject: Subject): void {
    this.selectedSubject = subject;
    this.selectedModule = null;
    this.selectedTopic = null;
  }

  selectModule(module: LearningModule): void {
    this.selectedModule = module;
    this.selectedTopic = null;
  }

  selectTopic(topic: LearningTopic): void {
    this.selectedTopic = topic;
    // Navigate to first level of the topic
    if (topic.levels.length > 0) {
      const firstLevel = topic.levels[0];
      this.router.navigate(['/learning', this.selectedModule?.id, topic.id, 'level', firstLevel.level]);
    }
  }

  goBack(): void {
    if (this.selectedTopic) {
      this.selectedTopic = null;
    } else if (this.selectedModule) {
      this.selectedModule = null;
    } else if (this.selectedSubject) {
      this.selectedSubject = null;
    }
  }

  getMiniNotes(atom: LearningAtom): string[] {
    const tags = ['Reference:', 'Online:', 'Quick note:'];
    return (atom.teachingStrategies || [])
      .filter(s => tags.some(t => s.startsWith(t)))
      .slice(0, 3);
  }
}
