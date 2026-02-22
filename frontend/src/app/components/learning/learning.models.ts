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
  notesTopicId?: string;   // if set, a "Download Notes PDF" button is shown

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

export interface LearningTopic {
  id: string;
  name: string;
  description: string;
  icon: string;
  levels: LearningAtom[];  // Each level has video, notes, practice, challenge
}

export interface LearningModule {
  id: string;
  name: string;
  description: string;
  icon: string;
  progress: number;
  atoms?: LearningAtom[];  // For modules without topics
  topics?: LearningTopic[];  // For modules with topics (like Four Operations)
}

export interface Subject {
  id: string;
  name: string;
  icon: string;
  description: string;
  modules: LearningModule[];
}
