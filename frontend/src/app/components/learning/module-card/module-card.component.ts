import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';
import { LearningModule } from '../learning.models';

const CARD_COLOURS = [
  'linear-gradient(135deg,#ff7043,#ff8a65)',
  'linear-gradient(135deg,#8e24aa,#ab47bc)',
  'linear-gradient(135deg,#00897b,#26a69a)',
  'linear-gradient(135deg,#1e88e5,#42a5f5)',
  'linear-gradient(135deg,#43a047,#66bb6a)',
  'linear-gradient(135deg,#e53935,#ef5350)',
  'linear-gradient(135deg,#f57c00,#ffa726)',
  'linear-gradient(135deg,#6d4c41,#8d6e63)',
];

@Component({
  selector: 'app-module-card',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './module-card.component.html',
  styleUrls: ['./module-card.component.scss']
})
export class ModuleCardComponent {
  @Input({ required: true }) module!: LearningModule;
  @Input() isAdmin = false;
  @Input() cardIndex = 0;

  get cardStyle(): { background: string } {
    return { background: CARD_COLOURS[this.cardIndex % CARD_COLOURS.length] };
  }
}
