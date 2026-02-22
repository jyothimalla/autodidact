export interface YearPolicy {
  year: number;
  benchmarkScore: number;
  goodThreshold: number;
  strongThreshold: number;
  subjectTargetThreshold: number;
  minActiveDays: number;
  minWeeklyMocks: number;
  weakTopicCount: number;
  targetLearningMinutes: number;
  sessionMinutes: number;
  timetableDays: string[];
}

const defaultDays = ['Monday', 'Tuesday', 'Thursday', 'Saturday'];

export const YEAR_POLICIES: Record<number, YearPolicy> = {
  1: { year: 1, benchmarkScore: 56, goodThreshold: 55, strongThreshold: 70, subjectTargetThreshold: 55, minActiveDays: 3, minWeeklyMocks: 0, weakTopicCount: 2, targetLearningMinutes: 90, sessionMinutes: 20, timetableDays: ['Monday', 'Wednesday', 'Friday'] },
  2: { year: 2, benchmarkScore: 58, goodThreshold: 57, strongThreshold: 72, subjectTargetThreshold: 57, minActiveDays: 3, minWeeklyMocks: 0, weakTopicCount: 2, targetLearningMinutes: 100, sessionMinutes: 22, timetableDays: ['Monday', 'Wednesday', 'Friday'] },
  3: { year: 3, benchmarkScore: 62, goodThreshold: 60, strongThreshold: 75, subjectTargetThreshold: 60, minActiveDays: 4, minWeeklyMocks: 1, weakTopicCount: 3, targetLearningMinutes: 140, sessionMinutes: 28, timetableDays: defaultDays },
  4: { year: 4, benchmarkScore: 66, goodThreshold: 64, strongThreshold: 78, subjectTargetThreshold: 64, minActiveDays: 4, minWeeklyMocks: 1, weakTopicCount: 3, targetLearningMinutes: 180, sessionMinutes: 35, timetableDays: ['Monday', 'Tuesday', 'Thursday', 'Saturday'] },
  5: { year: 5, benchmarkScore: 68, goodThreshold: 66, strongThreshold: 80, subjectTargetThreshold: 66, minActiveDays: 4, minWeeklyMocks: 1, weakTopicCount: 3, targetLearningMinutes: 200, sessionMinutes: 40, timetableDays: ['Monday', 'Tuesday', 'Thursday', 'Saturday'] },
  6: { year: 6, benchmarkScore: 70, goodThreshold: 68, strongThreshold: 82, subjectTargetThreshold: 68, minActiveDays: 5, minWeeklyMocks: 1, weakTopicCount: 3, targetLearningMinutes: 220, sessionMinutes: 42, timetableDays: ['Monday', 'Tuesday', 'Wednesday', 'Friday', 'Sunday'] },
  7: { year: 7, benchmarkScore: 72, goodThreshold: 70, strongThreshold: 83, subjectTargetThreshold: 70, minActiveDays: 4, minWeeklyMocks: 1, weakTopicCount: 3, targetLearningMinutes: 210, sessionMinutes: 40, timetableDays: defaultDays },
  8: { year: 8, benchmarkScore: 73, goodThreshold: 71, strongThreshold: 84, subjectTargetThreshold: 71, minActiveDays: 4, minWeeklyMocks: 1, weakTopicCount: 3, targetLearningMinutes: 220, sessionMinutes: 42, timetableDays: defaultDays },
  9: { year: 9, benchmarkScore: 74, goodThreshold: 72, strongThreshold: 85, subjectTargetThreshold: 72, minActiveDays: 5, minWeeklyMocks: 1, weakTopicCount: 3, targetLearningMinutes: 240, sessionMinutes: 45, timetableDays: ['Monday', 'Tuesday', 'Thursday', 'Friday', 'Sunday'] },
  10: { year: 10, benchmarkScore: 76, goodThreshold: 74, strongThreshold: 86, subjectTargetThreshold: 74, minActiveDays: 5, minWeeklyMocks: 1, weakTopicCount: 4, targetLearningMinutes: 260, sessionMinutes: 50, timetableDays: ['Monday', 'Tuesday', 'Wednesday', 'Friday', 'Sunday'] },
  11: { year: 11, benchmarkScore: 78, goodThreshold: 75, strongThreshold: 88, subjectTargetThreshold: 75, minActiveDays: 5, minWeeklyMocks: 2, weakTopicCount: 4, targetLearningMinutes: 300, sessionMinutes: 55, timetableDays: ['Monday', 'Tuesday', 'Wednesday', 'Friday', 'Saturday'] },
  12: { year: 12, benchmarkScore: 80, goodThreshold: 77, strongThreshold: 89, subjectTargetThreshold: 77, minActiveDays: 5, minWeeklyMocks: 2, weakTopicCount: 4, targetLearningMinutes: 320, sessionMinutes: 60, timetableDays: ['Monday', 'Tuesday', 'Thursday', 'Friday', 'Sunday'] },
  13: { year: 13, benchmarkScore: 82, goodThreshold: 78, strongThreshold: 90, subjectTargetThreshold: 78, minActiveDays: 6, minWeeklyMocks: 2, weakTopicCount: 4, targetLearningMinutes: 360, sessionMinutes: 60, timetableDays: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday'] },
};

export function getYearPolicy(year: number): YearPolicy {
  if (year < 1) return YEAR_POLICIES[1];
  if (year > 13) return YEAR_POLICIES[13];
  return YEAR_POLICIES[year];
}
