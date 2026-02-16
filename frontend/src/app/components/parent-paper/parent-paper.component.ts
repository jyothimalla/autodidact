import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { LEARNING_MODULES } from '../learning/learning.data';
import { AuthService } from '../../auth/auth.service';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-parent-paper',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './parent-paper.component.html',
  styleUrls: ['./parent-paper.component.scss']
})
export class ParentPaperComponent {
  readonly modules = LEARNING_MODULES;
  readonly numOptions = [5, 10, 15, 20];
  readonly difficulties = ['easy', 'medium', 'hard'];

  selectedModule = this.modules[0].id;
  selectedNum = 10;
  selectedDifficulty = 'medium';

  isGenerating = false;
  paperId: string | null = null;
  paperDbId: number | null = null;
  paperModule = '';
  errorMessage = '';

  private readonly apiBase = environment.apiBaseUrl;

  constructor(private http: HttpClient, private auth: AuthService) {}

  get userId(): number {
    return this.auth.getUserId() ?? 0;
  }

  get selectedModuleName(): string {
    return this.modules.find(m => m.id === this.selectedModule)?.name ?? '';
  }

  generatePaper(): void {
    this.errorMessage = '';
    this.paperId = null;
    this.isGenerating = true;

    this.http.post<any>(`${this.apiBase}/paper/custom/generate`, {
      user_id: this.userId,
      module_id: this.selectedModule,
      num_questions: this.selectedNum,
      difficulty: this.selectedDifficulty
    }).subscribe({
      next: (res) => {
        this.paperId = res.paper_id;
        this.paperDbId = res.id;
        this.paperModule = res.module;
        this.isGenerating = false;
      },
      error: (err) => {
        this.errorMessage = err?.error?.detail ?? 'Failed to generate paper. Please try again.';
        this.isGenerating = false;
      }
    });
  }

  downloadQuestionPaper(): void {
    if (!this.paperId) return;
    const name = `${this.paperModule}_${this.paperId}_id${this.paperDbId}_questions.pdf`;
    this._downloadBlob(`${this.apiBase}/paper/custom/${this.paperId}/question-pdf`, name);
  }

  downloadAnswerSheet(): void {
    if (!this.paperId) return;
    const name = `${this.paperModule}_${this.paperId}_id${this.paperDbId}_answer_sheet.pdf`;
    this._downloadBlob(`${this.apiBase}/paper/custom/${this.paperId}/answer-sheet-pdf`, name);
  }

  private _downloadBlob(url: string, filename: string): void {
    this.http.get(url, { responseType: 'blob' }).subscribe({
      next: (blob) => {
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = filename;
        a.click();
        URL.revokeObjectURL(a.href);
      },
      error: () => {
        this.errorMessage = 'Download failed. Please try again.';
      }
    });
  }
}
