import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';
import { LearningSubSkill, MasteryStatus } from '../learning.models';

@Component({
  selector: 'app-subskill-card',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './subskill-card.component.html',
  styleUrls: ['./subskill-card.component.scss']
})
export class SubskillCardComponent {
  @Input({ required: true }) subskill!: LearningSubSkill;
  @Input({ required: true }) moduleId!: string;
  @Input() isAdmin = false;

  badgeLabel(status: MasteryStatus): string {
    if (status === 'weak') return 'Weak';
    if (status === 'strong') return 'Strong';
    return 'Developing';
  }
}
