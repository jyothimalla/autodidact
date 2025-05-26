import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UploadAnswersComponent } from './upload-answers/upload-answers.component';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule, FormsModule, UploadAnswersComponent],
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.scss']
})
export class AnalyticsComponent {
  selectedTab = 'questions';
  
  tabs = [
    { label: 'Usage', key: 'usage' },
    { label: 'Trouble Spots', key: 'trouble' },
    { label: 'Scores', key: 'scores' },
    { label: 'Questions', key: 'questions' },
    { label: 'Progress', key: 'progress' }
  ];

currentTab: string = 'usage';

setTab(tab: string) {
  this.currentTab = tab;
}
activeTab: string = 'summary';


}
