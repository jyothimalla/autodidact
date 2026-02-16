import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';
import { ExampleService } from '../../services/example.service';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { combineLatest } from 'rxjs';

interface LearningModule {
  title: string;
  objective: string;
  tips: string[];
}

@Component({
  selector: 'app-learn',
  standalone: true,
  imports: [CommonModule, LeftSidebarComponent],
  templateUrl: './learn.component.html',
  styleUrls: ['./learn.component.scss']
})
export class LearnComponent implements OnInit {
  level = 0;
  username = '';
  user_id = 0;
  operation = 'addition';
  videoFinished = false;
  example: { question: string; answer: number } | null = null;
  youtubeUrl: SafeResourceUrl | null = null;

  readonly learningModules: Record<string, LearningModule> = {
    addition: {
      title: 'Addition Basics',
      objective: 'Learn how to combine numbers confidently from simple sums to carrying.',
      tips: ['Line up place values before adding.', 'Add from right to left.', 'Carry only when sum is 10 or more.']
    },
    subtraction: {
      title: 'Subtraction Basics',
      objective: 'Understand subtraction as taking away and as finding the difference.',
      tips: ['Start from ones column.', 'Borrow from the next column only when needed.', 'Check with inverse addition.']
    },
    multiplication: {
      title: 'Multiplication Basics',
      objective: 'Build quick multiplication thinking using repeated addition and patterns.',
      tips: ['Know key tables (2, 5, 10) first.', 'Break larger factors into smaller chunks.', 'Use place-value alignment for multi-digit multiplication.']
    },
    division: {
      title: 'Division Basics',
      objective: 'Practice splitting into equal groups and understanding remainders.',
      tips: ['Use multiplication facts to estimate.', 'Divide from highest place value first.', 'Check by multiplying quotient with divisor.']
    },
    fmc: {
      title: 'Fast Mental Calculation',
      objective: 'Develop speed and number sense with structured mental strategies.',
      tips: ['Round numbers mentally, then adjust.', 'Use compensation methods.', 'Stay consistent with one strategy per problem type.']
    }
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private sanitizer: DomSanitizer,
    private exampleService: ExampleService
  ) {}

  ngOnInit(): void {
    combineLatest([this.route.paramMap, this.route.queryParams]).subscribe(([paramMap, queryParams]) => {
      const routeOperation = paramMap.get('operation') || paramMap.get('type') || queryParams['operation'] || 'addition';
      this.operation = this.normalizeOperation(routeOperation);
      this.level = parseInt(queryParams['level'] || '0', 10);
      this.username = queryParams['username'] || localStorage.getItem('username') || 'Guest';
      this.user_id = parseInt(queryParams['user_id'] || localStorage.getItem('user_id') || '0', 10);

      localStorage.setItem('operation', this.operation);
      this.setYoutubeUrl();
      this.example = this.exampleService.getExample(this.operation, this.level);
    });
  }

  get activeModule(): LearningModule {
    return this.learningModules[this.operation] || this.learningModules['addition'];
  }

  get imageSrc(): string {
    return `assets/images/${this.operation}_level${this.level}.png`;
  }

  goBack(): void {
    window.history.back();
  }

  onVideoEnd(): void {
    this.videoFinished = true;
    console.log('✅ Video completed for level', this.level);
  }

  tryPractice(): void {
    this.router.navigate([`/practice/${this.operation}`], {
      queryParams: {
        level: this.level,
        username: this.username,
        user_id: this.user_id
      }
    });
  }
  
  goToPractice(): void {
    this.router.navigate([`/practice/${this.operation}`], {
      queryParams: {
        level: this.level,
        username: this.username,
        user_id: this.user_id
      }
    });
  }
  takeChallenge(): void {
    this.router.navigate([`/${this.operation}`], {
      queryParams: {
        level: this.level,
        username: this.username,
        user_id: this.user_id
      }
    });
  }
  youtubeVideoId(): string {
    const videoIdMap: { [key: string]: string } = {
      addition: 'videoId1',
      subtraction: 'videoId2',
      multiplication: 'videoId3',
      division: 'videoId4'
    };
    return videoIdMap[this.operation] || '';
  }
  getYoutubeIdFromUrl(url: string): string {
    const regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : '';
  }

  readonly youtubeVideoMap: { [operation: string]: { [level: number]: string } } = {
  addition: {
    0: 'NybHckSEQBI',  // Addition basics
    1: '_NN8g2jWIAs',  // Addition with carry
    2: 'BZ4FjSXjzgg',  // Addition with 3-digit numbers
    3: 'mAvuom42NyY',
    4: 'mAvuom42NyY',
    5: 'mAvuom42NyY',
    6: 'mAvuom42NyY',
    7: 'mAvuom42NyY',
    8: 'mAvuom42NyY',
    9: 'mAvuom42NyY',
  },
  subtraction: {
    0: 'Y6M89-6106I',
    1: '0JwoC9WlAYU',
    2: 'r3qKojj4g4g',
    3: 'r3qKojj4g4g',
    4: '5juto2ze8Lg',
    5: '_BgblvF90UE',
    6: '5juto2ze8Lg',
    7: '5juto2ze8Lg',
    8: '5juto2ze8Lg',
    9: '5juto2ze8Lg',

    // ...
  },
  multiplication: {
    0: 'EI2qZC1vUGk',
    1: 'kwh4SD1ToFc',
    2: 'kwh4SD1ToFc',
    3: 'kwh4SD1ToFc',
    4: 'qmfXyR7Z6Lk',
    5: 'kwh4SD1ToFc',
    6: 'kwh4SD1ToFc',
    7: 'kwh4SD1ToFc',
    8: 'kwh4SD1ToFc',
    9: 'kwh4SD1ToFc',
    // ...
  },
  division: {
    0: 'fb2XsYU0o8M',
    1: 'fb2XsYU0o8M',
    2: 'fb2XsYU0o8M',
    3:  'fb2XsYU0o8M',
    4: 'fb2XsYU0o8M',
    5: 'fb2XsYU0o8M',
    6: 'HdU_rf7eMTI',
    7:  'HdU_rf7eMTI',
    8: 'HdU_rf7eMTI',
    9: 'HdU_rf7eMTI',
    // ...
  },
  fmc: {
    0: 'fb2XsYU0o8M',
    1: 'fb2XsYU0o8M',
    2: 'fb2XsYU0o8M',
    3: 'fb2XsYU0o8M',
    4: 'fb2XsYU0o8M',
    5: 'fb2XsYU0o8M',
    6: 'HdU_rf7eMTI',
    7: 'HdU_rf7eMTI',
    8: 'HdU_rf7eMTI',
    9: 'HdU_rf7eMTI',
    // ...
  }
};

  private normalizeOperation(operation: string): string {
    const normalized = (operation || '').toLowerCase().trim();
    return this.learningModules[normalized] ? normalized : 'addition';
  }

  private setYoutubeUrl(): void {
    const videoId = this.youtubeVideoMap[this.operation]?.[this.level];
    this.youtubeUrl = videoId
      ? this.sanitizer.bypassSecurityTrustResourceUrl(`https://www.youtube.com/embed/${videoId}`)
      : null;
  }
}
