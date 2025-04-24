import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProgressService, UserProgress, LevelAttempt } from './progress.service';
import { FormsModule } from '@angular/forms';
import Chart from 'chart.js/auto';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

@Component({
  selector: 'app-progress',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './progress.component.html'
})
export class ProgressComponent implements OnInit {
  progress: UserProgress[] = [];
  attempts: LevelAttempt[] = [];
  filteredAttempts: LevelAttempt[] = [];
  username = localStorage.getItem('username') || '';
  filterOperation: string = '';
  operations: string[] = [];

  constructor(private progressService: ProgressService) {}

  ngOnInit() {
    if (this.username) {
      this.progressService.getProgress(this.username).subscribe(res => {
        this.progress = res;
        this.operations = [...new Set(res.map(p => p.operation))];
        setTimeout(() => {
          this.renderLevelChart();
          this.renderAverageScoreChart();
        }, 0);
      });

      this.progressService.getAttempts(this.username).subscribe(res => {
        this.attempts = res;
        this.filteredAttempts = res;
      });
    }
  }

  applyFilter() {
    this.filteredAttempts = this.filterOperation
      ? this.attempts.filter(a => a.operation.toLowerCase() === this.filterOperation.toLowerCase())
      : this.attempts;
  }

  exportCSV() {
    const headers = ['Operation', 'Level', 'Attempt', 'Score', 'Passed', 'Date'];
    const rows = this.filteredAttempts.map(a => [
      a.operation,
      a.level,
      a.attempt_number,
      `${a.score}/${a.total_questions}`,
      a.is_passed ? 'Yes' : 'No',
      new Date(a.timestamp).toLocaleString()
    ]);

    const csvContent = [headers, ...rows].map(e => e.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `attempt-history-${this.username}.csv`);
    link.click();
  }

  exportPDF() {
    const doc = new jsPDF();
    doc.text(`Attempt History - ${this.username}`, 10, 10);
    const rows = this.filteredAttempts.map(a => [
      a.operation,
      a.level,
      a.attempt_number,
      `${a.score}/${a.total_questions}`,
      a.is_passed ? 'Yes' : 'No',
      new Date(a.timestamp).toLocaleString()
    ]);
    (doc as any).autoTable({
      head: [['Operation', 'Level', 'Attempt', 'Score', 'Passed', 'Date']],
      body: rows,
    });
    doc.save(`attempt-history-${this.username}.pdf`);
  }

  renderLevelChart() {
    const ctx = document.getElementById('progressChart') as HTMLCanvasElement;
    if (!ctx) return;
    const labels = this.progress.map(p => p.operation);
    const levels = this.progress.map(p => p.level_completed);

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Level Completed',
          data: levels,
          backgroundColor: '#4caf50'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }

  renderAverageScoreChart() {
    const ctx = document.getElementById('scoreChart') as HTMLCanvasElement;
    if (!ctx) return;
    const grouped: { [key: string]: number[] } = {};
    this.attempts.forEach(a => {
      if (!grouped[a.operation]) grouped[a.operation] = [];
      grouped[a.operation].push((a.score / a.total_questions) * 100);
    });
    const labels = Object.keys(grouped);
    const averages = labels.map(op => {
      const scores = grouped[op];
      return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
    });

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Avg. Score %',
          data: averages,
          backgroundColor: '#2196f3'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    });
  }
}
