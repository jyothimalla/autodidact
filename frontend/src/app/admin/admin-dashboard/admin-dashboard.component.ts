import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProgressService, LevelAttempt } from '../../progress/progress.service';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './admin-dashboard.component.html'
})
export class AdminDashboardComponent implements OnInit {
  allAttempts: LevelAttempt[] = [];
  filtered: LevelAttempt[] = [];
  filterUser: string = '';
  filterOp: string = '';
  operations: string[] = [];

  constructor(private progressService: ProgressService, private route: ActivatedRoute ) {}

  ngOnInit() {
    this.progressService.getAllAttempts().subscribe(res => {
      this.allAttempts = res;
      this.filtered = res;
      this.operations = [...new Set(res.map(a => a.operation))];  // ✅ unique ops
    });
    
  }

  applyFilter() {
    this.filtered = this.allAttempts.filter(a =>
      (!this.filterUser || a.user_name.toLowerCase().includes(this.filterUser.toLowerCase())) &&
      (!this.filterOp || a.operation.toLowerCase() === this.filterOp.toLowerCase())
    );
  }
}
