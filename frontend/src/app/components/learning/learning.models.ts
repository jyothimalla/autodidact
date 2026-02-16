export type MasteryStatus = 'weak' | 'developing' | 'strong';

export interface LearningAtom {
  id: string;
  moduleId: string;
  name: string;
  level: number;
  status: MasteryStatus;

  // Student-facing fields
  summary: string;
  videoUrl: string;

  // Teacher-only fields (rendered only when isAdmin === true)
  teachingNotes: string;
  commonMistakes: string[];
  prerequisites: string[];
  teachingStrategies: string[];
  assessmentCriteria: string;
  estimatedMinutes: number;
}

/** Backward-compatible alias */
export type LearningSubSkill = LearningAtom;

export interface LearningModule {
  id: string;
  name: string;
  description: string;
  icon: string;
  progress: number;
  atoms: LearningAtom[];
}
