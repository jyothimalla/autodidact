import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { forkJoin, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { getYearPolicy, type YearPolicy } from './year-plan.policy';

interface MockTestResult {
  test_id: string;
  score: number;
  total: number;
  percentage: number;
  time_taken: number;
  submitted_at: string;
}

interface PracticeHistoryItem {
  attempt_id: string;
  subject_id: string;
  module_id: string;
  attempt_type: string;
  num_questions: number;
  score: number | null;
  percentage: number | null;
  created_at: string | null;
  submitted_at: string | null;
  status: 'submitted' | 'pending';
}

interface ModuleAnalytics {
  attempts: number;
  score: number;
  total: number;
  percentage: number;
}

interface SubjectAnalytics {
  total_attempts: number;
  total_score: number;
  total_questions: number;
  avg_percentage: number;
  by_module: Record<string, ModuleAnalytics>;
}

interface PracticeAnalyticsResponse {
  [subjectId: string]: SubjectAnalytics;
}

interface SubjectCard {
  label: string;
  key: string;
  score: number;
  status: string;
}

interface TimelinePoint {
  label: string;
  benchmark: number;
}

interface YearPlanView {
  benchmark: number;
  activeDays: number;
  weeklyMocks: number;
  weeklyMinutes: number;
}

interface TimetableSlot {
  day: string;
  focus: string;
  duration: number;
}

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.scss']
})
export class AnalyticsComponent implements OnInit {
  private readonly apiBase = environment.apiBaseUrl;
  private readonly yearStorageKey = 'student_year';

  loading = true;
  errorMessage = '';

  studentName = localStorage.getItem('username') || 'Student';
  userId = Number(localStorage.getItem('user_id') || 0);

  yearLevels = Array.from({ length: 13 }, (_, i) => i + 1);
  selectedYear = 6;

  activeDays = 0;
  learningMinutes = 0;
  questionsAnswered = 0;
  islandsCompleted = 0;
  targetsMet: string[] = [];
  mockTestsCompleted = 0;
  customPracticesCompleted = 0;

  performanceLabel = 'On track';
  performanceScore = 0;
  benchmarkScore = 66;

  subjects: SubjectCard[] = [
    { label: 'English', key: 'english', score: 0, status: 'No data' },
    { label: 'VR', key: 'vr', score: 0, status: 'No data' },
    { label: 'Maths', key: 'maths', score: 0, status: 'No data' },
    { label: 'NVR', key: 'nvr', score: 0, status: 'No data' },
    { label: 'Science', key: 'science', score: 0, status: 'No data' }
  ];

  weakTopics: string[] = [];
  recommendations: string[] = [];

  examTopicsDoneThisWeek = 0;
  weeklyTopicItems: Array<{ title: string; when: string }> = [];
  testsDoneThisWeek = 0;
  weeklyTestItems: Array<{ title: string; score: string; when: string }> = [];

  timeline: TimelinePoint[] = [];
  yearPlan: YearPlanView = { benchmark: 66, activeDays: 4, weeklyMocks: 1, weeklyMinutes: 180 };
  needsAttentionTargets: string[] = [];
  needsAttentionTimetable: TimetableSlot[] = [];

  private mockResultsCache: MockTestResult[] = [];
  private practiceHistoryCache: PracticeHistoryItem[] = [];
  private practiceAnalyticsCache: PracticeAnalyticsResponse = {};

  constructor(private readonly http: HttpClient) {}

  ngOnInit(): void {
    const candidate = Number(localStorage.getItem(this.yearStorageKey));

    if (candidate >= 1 && candidate <= 13) {
      this.selectedYear = candidate;
    }

    this.applyYearPolicy();

    if (!this.userId) {
      this.loading = false;
      this.errorMessage = 'No logged-in user found. Please login first.';
      return;
    }

    this.loadAnalytics();
  }

  onYearChange(event: Event): void {
    const value = Number((event.target as HTMLSelectElement).value);
    if (value < 1 || value > 13) {
      return;
    }

    this.selectedYear = value;
    localStorage.setItem(this.yearStorageKey, String(value));
    // backward-compat for older key usage
    localStorage.setItem('analytics_year_level', String(value));

    this.applyYearPolicy();
    this.recomputeFromCache();
  }

  private applyYearPolicy(): void {
    const policy = this.currentPolicy;
    this.benchmarkScore = policy.benchmarkScore;
    this.yearPlan = {
      benchmark: policy.benchmarkScore,
      activeDays: policy.minActiveDays,
      weeklyMocks: policy.minWeeklyMocks,
      weeklyMinutes: policy.targetLearningMinutes
    };
    this.timeline = [
      { label: 'Sep', benchmark: policy.benchmarkScore - 10 },
      { label: 'Oct', benchmark: policy.benchmarkScore - 8 },
      { label: 'Nov', benchmark: policy.benchmarkScore - 6 },
      { label: 'Dec', benchmark: policy.benchmarkScore - 4 },
      { label: 'Jan', benchmark: policy.benchmarkScore - 2 },
      { label: 'Feb', benchmark: policy.benchmarkScore },
      { label: 'Mar', benchmark: policy.benchmarkScore + 2 }
    ];
  }

  private loadAnalytics(): void {
    this.loading = true;

    forkJoin({
      mockResults: this.http
        .get<MockTestResult[]>(`${this.apiBase}/test/results/${this.userId}`)
        .pipe(catchError(() => of([]))),
      practiceHistory: this.http
        .get<PracticeHistoryItem[]>(`${this.apiBase}/practice/history/${this.userId}`)
        .pipe(catchError(() => of([]))),
      practiceAnalytics: this.http
        .get<PracticeAnalyticsResponse>(`${this.apiBase}/practice/analytics/${this.userId}`)
        .pipe(catchError(() => of({})))
    }).subscribe({
      next: ({ mockResults, practiceHistory, practiceAnalytics }) => {
        this.mockResultsCache = mockResults;
        this.practiceHistoryCache = practiceHistory;
        this.practiceAnalyticsCache = practiceAnalytics;

        this.recomputeFromCache();
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Unable to load analytics right now.';
        this.loading = false;
      }
    });
  }

  private recomputeFromCache(): void {
    this.computeSummary(this.mockResultsCache, this.practiceHistoryCache, this.practiceAnalyticsCache);
    this.computeSubjects(this.practiceAnalyticsCache);
    this.computeWeakTopics(this.practiceAnalyticsCache);
    this.computeWeeklyActivities(this.mockResultsCache, this.practiceHistoryCache);
    this.computePerformance(this.mockResultsCache, this.practiceHistoryCache);
    this.buildRecommendations();
    this.buildNeedsAttentionPlan();
  }

  private get currentPolicy(): YearPolicy {
    return getYearPolicy(this.selectedYear);
  }

  private computeSummary(
    mockResults: MockTestResult[],
    practiceHistory: PracticeHistoryItem[],
    practiceAnalytics: PracticeAnalyticsResponse
  ): void {
    const now = new Date();
    const weekAgo = new Date(now);
    weekAgo.setDate(now.getDate() - 6);

    const weekEvents: string[] = [];
    for (const p of practiceHistory) {
      if (p.created_at && new Date(p.created_at) >= weekAgo) {
        weekEvents.push(p.created_at);
      }
      if (p.submitted_at && new Date(p.submitted_at) >= weekAgo) {
        weekEvents.push(p.submitted_at);
      }
    }
    for (const m of mockResults) {
      if (m.submitted_at && new Date(m.submitted_at) >= weekAgo) {
        weekEvents.push(m.submitted_at);
      }
    }

    const uniqueDays = new Set(weekEvents.map((ts) => ts.slice(0, 10)));
    this.activeDays = uniqueDays.size;

    const practiceSubmitted = practiceHistory.filter((item) => item.status === 'submitted');
    const practiceQuestions = practiceSubmitted.reduce((sum, item) => sum + item.num_questions, 0);
    const mockQuestions = mockResults.reduce((sum, item) => sum + item.total, 0);

    this.questionsAnswered = practiceQuestions + mockQuestions;
    this.islandsCompleted = practiceSubmitted.length;
    this.mockTestsCompleted = mockResults.length;
    this.customPracticesCompleted = practiceSubmitted.filter((item) => item.attempt_type === 'practice').length;

    const mockMinutes = Math.round(mockResults.reduce((sum, item) => sum + (item.time_taken || 0), 0) / 60);
    const practiceEstimatePerAttempt = this.selectedYear <= 6 ? 7 : 10;
    const estimatedPracticeMinutes = practiceSubmitted.length * practiceEstimatePerAttempt;
    this.learningMinutes = mockMinutes + estimatedPracticeMinutes;

    this.targetsMet = this.extractMetTargets(practiceAnalytics);
  }

  private computeSubjects(practiceAnalytics: PracticeAnalyticsResponse): void {
    const aggregate: Record<string, { scoreSum: number; questionSum: number }> = {
      english: { scoreSum: 0, questionSum: 0 },
      vr: { scoreSum: 0, questionSum: 0 },
      maths: { scoreSum: 0, questionSum: 0 },
      nvr: { scoreSum: 0, questionSum: 0 },
      science: { scoreSum: 0, questionSum: 0 }
    };

    Object.entries(practiceAnalytics).forEach(([subjectId, subjectData]) => {
      const mapped = this.mapSubjectKey(subjectId);
      if (!mapped) {
        return;
      }
      aggregate[mapped].scoreSum += subjectData.total_score;
      aggregate[mapped].questionSum += subjectData.total_questions;
    });

    this.subjects = this.subjects.map((subject) => {
      const total = aggregate[subject.key].questionSum;
      if (!total) {
        return { ...subject, score: 0, status: 'No data' };
      }

      const pct = Math.round((aggregate[subject.key].scoreSum / total) * 100);
      let status = 'Needs focus';
      if (pct >= this.currentPolicy.strongThreshold) {
        status = 'Strong';
      } else if (pct >= this.currentPolicy.goodThreshold) {
        status = 'Good';
      }

      return { ...subject, score: pct, status };
    });
  }

  private computeWeakTopics(practiceAnalytics: PracticeAnalyticsResponse): void {
    const moduleRows: Array<{ module: string; percentage: number }> = [];

    Object.values(practiceAnalytics).forEach((subject) => {
      Object.entries(subject.by_module || {}).forEach(([moduleId, moduleStats]) => {
        moduleRows.push({ module: moduleId, percentage: moduleStats.percentage ?? 0 });
      });
    });

    this.weakTopics = moduleRows
      .sort((a, b) => a.percentage - b.percentage)
      .slice(0, this.currentPolicy.weakTopicCount)
      .map((row) => this.prettifyModule(row.module));
  }

  private computeWeeklyActivities(
    mockResults: MockTestResult[],
    practiceHistory: PracticeHistoryItem[]
  ): void {
    const now = new Date();
    const weekAgo = new Date(now);
    weekAgo.setDate(now.getDate() - 6);

    const weeklyPractice = practiceHistory
      .filter((item) => item.submitted_at && new Date(item.submitted_at) >= weekAgo)
      .sort((a, b) => (b.submitted_at || '').localeCompare(a.submitted_at || ''));

    const weeklyMocks = mockResults
      .filter((item) => item.submitted_at && new Date(item.submitted_at) >= weekAgo)
      .sort((a, b) => (b.submitted_at || '').localeCompare(a.submitted_at || ''));

    this.examTopicsDoneThisWeek = new Set(weeklyPractice.map((item) => item.module_id)).size;
    this.testsDoneThisWeek = weeklyMocks.length;

    this.weeklyTopicItems = weeklyPractice.slice(0, 2).map((item) => ({
      title: this.prettifyModule(item.module_id),
      when: this.relativeDay(item.submitted_at)
    }));

    this.weeklyTestItems = weeklyMocks.slice(0, 2).map((item) => ({
      title: `Mock Test ${item.test_id.slice(-4).toUpperCase()}`,
      score: `${item.score}/${item.total}`,
      when: this.relativeDay(item.submitted_at)
    }));
  }

  private computePerformance(mockResults: MockTestResult[], practiceHistory: PracticeHistoryItem[]): void {
    const practiceSubmitted = practiceHistory.filter((item) => item.status === 'submitted');

    const practiceCorrect = practiceSubmitted.reduce((sum, item) => sum + (item.score || 0), 0);
    const practiceTotal = practiceSubmitted.reduce((sum, item) => sum + item.num_questions, 0);

    const mockCorrect = mockResults.reduce((sum, item) => sum + item.score, 0);
    const mockTotal = mockResults.reduce((sum, item) => sum + item.total, 0);

    const totalQuestions = practiceTotal + mockTotal;
    const totalCorrect = practiceCorrect + mockCorrect;

    this.performanceScore = totalQuestions ? Math.round((totalCorrect / totalQuestions) * 100) : 0;

    if (this.performanceScore >= this.benchmarkScore + 6) {
      this.performanceLabel = 'Strong progress';
    } else if (this.performanceScore >= this.benchmarkScore) {
      this.performanceLabel = 'On track';
    } else if (this.performanceScore >= this.benchmarkScore - 5) {
      this.performanceLabel = 'Close to target';
    } else {
      this.performanceLabel = 'Needs attention';
    }
  }

  private buildRecommendations(): void {
    const policy = this.currentPolicy;
    const recommendations: string[] = [];

    if (this.activeDays < policy.minActiveDays) {
      recommendations.push(`${this.studentName} should aim to log in at least ${policy.minActiveDays} days each week for Year ${this.selectedYear}.`);
    } else {
      recommendations.push(`${this.studentName} is maintaining a strong weekly study routine for Year ${this.selectedYear}.`);
    }

    if (this.learningMinutes < policy.targetLearningMinutes) {
      recommendations.push(`Increase weekly study time toward ${policy.targetLearningMinutes} minutes to stay aligned with Year ${this.selectedYear} targets.`);
    } else {
      recommendations.push(`Weekly study time is healthy for Year ${this.selectedYear}. Keep this pace consistent.`);
    }

    if (this.testsDoneThisWeek < policy.minWeeklyMocks) {
      recommendations.push(`Complete at least ${policy.minWeeklyMocks} mock test${policy.minWeeklyMocks === 1 ? '' : 's'} per week.`);
    } else {
      recommendations.push('Mock-test routine is on track. Continue regular exam practice.');
    }

    if (this.weakTopics.length > 0) {
      recommendations.push(`${this.studentName} needs focused practice in: ${this.weakTopics.join(', ')}.`);
    } else {
      recommendations.push('Current topic performance is balanced across recent activity.');
    }

    this.recommendations = recommendations;
  }

  private buildNeedsAttentionPlan(): void {
    const policy = this.currentPolicy;
    const dailyMinutes = Math.ceil(policy.targetLearningMinutes / Math.max(policy.minActiveDays, 1));
    const dailyQuestionTarget = this.selectedYear <= 4 ? 25 : this.selectedYear <= 8 ? 35 : 45;
    const weeklyPracticeTarget = this.selectedYear <= 4 ? 4 : this.selectedYear <= 8 ? 5 : 6;

    this.needsAttentionTargets = [
      `Daily focus: ${dailyMinutes} minutes and ${dailyQuestionTarget} questions on practice days.`,
      `Weekly consistency: ${policy.minActiveDays} active day(s), ${policy.minWeeklyMocks} mock test(s), ${weeklyPracticeTarget} practice set(s).`,
      `Subject threshold: keep each subject at or above ${policy.subjectTargetThreshold}% for Year ${this.selectedYear}.`,
      'Escalation rule: if below target for 2 consecutive weeks, add one extra practice day and one extra mock.'
    ];

    const focusTopics = this.weakTopics.length > 0 ? this.weakTopics : ['Core Maths', 'Core English'];
    this.needsAttentionTimetable = policy.timetableDays.map((day, idx) => ({
      day,
      focus: focusTopics[idx % focusTopics.length],
      duration: policy.sessionMinutes
    }));
  }

  private extractMetTargets(practiceAnalytics: PracticeAnalyticsResponse): string[] {
    const met = new Set<string>();

    Object.entries(practiceAnalytics).forEach(([subjectId, summary]) => {
      if (!summary.total_questions) {
        return;
      }
      const pct = (summary.total_score / summary.total_questions) * 100;
      if (pct >= this.currentPolicy.subjectTargetThreshold) {
        const mapped = this.mapSubjectKey(subjectId);
        if (!mapped) {
          return;
        }
        const label = this.subjects.find((s) => s.key === mapped)?.label;
        if (label) {
          met.add(label);
        }
      }
    });

    return [...met];
  }

  private mapSubjectKey(subjectId: string): string | null {
    const raw = (subjectId || '').toLowerCase();
    if (raw.includes('english')) return 'english';
    if (raw.includes('math')) return 'maths';
    if (raw.includes('science')) return 'science';
    if (raw.includes('non-verbal') || raw.includes('nvr')) return 'nvr';
    if (raw.includes('verbal') || raw === 'vr') return 'vr';
    return null;
  }

  private prettifyModule(moduleId: string): string {
    return moduleId
      .replace(/-/g, ' ')
      .replace(/\b\w/g, (letter: string) => letter.toUpperCase());
  }

  private relativeDay(isoDate: string | null): string {
    if (!isoDate) {
      return '';
    }

    const d = new Date(isoDate);
    const today = new Date();
    const todayKey = today.toISOString().slice(0, 10);

    const y = new Date();
    y.setDate(today.getDate() - 1);
    const yesterdayKey = y.toISOString().slice(0, 10);

    const dateKey = d.toISOString().slice(0, 10);
    if (dateKey === todayKey) return 'Today';
    if (dateKey === yesterdayKey) return 'Yesterday';
    return d.toLocaleDateString();
  }

  get progressBarWidth(): number {
    return Math.max(5, Math.min(100, this.performanceScore));
  }

  trackBySubject(_: number, subject: SubjectCard): string {
    return subject.key;
  }
}
