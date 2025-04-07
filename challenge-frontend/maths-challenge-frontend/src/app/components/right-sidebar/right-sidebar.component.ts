import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-right-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './right-sidebar.component.html',
  styleUrls: ['./right-sidebar.component.scss']
})
export class RightSidebarComponent {
  @Input() userName: string = '';
  @Input() score: number = 0;
  @Input() currentQIndex: number = 0;
  @Input() totalQuestions: number = 0;
  @Input() elapsedTime: string = '0:00';
}
