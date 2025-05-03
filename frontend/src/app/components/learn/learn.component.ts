import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { LeftSidebarComponent } from '../left-sidebar/left-sidebar.component';
import { QuizService } from '../../services/quiz.service';
import { ExampleService } from '../../services/example.service';

import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';


@Component({
  selector: 'app-learn',
  standalone: true,
  imports: [CommonModule, LeftSidebarComponent],
  templateUrl: './learn.component.html',
  styleUrls: ['./learn.component.scss']
})
export class LearnComponent implements OnInit {
  level: number = 0;
  username: string = '';
  user_id: number = 0;
  operation: string = '';
  videoFinished: boolean = false;
  showExample: boolean = false;
  example: { question: string, answer: number } | null = null;  // ✅ properly declare example
  selectedOperation: string='';
  exampleHtml: string = `
    <p><strong>Example:</strong> 700 + 500 =</p>
    <p>Arrange:</p>
    <pre>700\n+500</pre>
    <p>Add zeros, then add 7 + 5 = 12</p>
  `;
  constructor(private route: ActivatedRoute, private router: Router,
              private quizService: QuizService,
              private sanitizer: DomSanitizer,

              private exampleService: ExampleService,
  ) {}

  ngOnInit(): void {
   
    this.route.queryParams.subscribe(params => {
      this.level = parseInt(params['level'] || '0', 10);
      this.username = this.route.snapshot.queryParams['username'] || localStorage.getItem('username') || '';
      this.user_id = parseInt(localStorage.getItem('user_id') || '0', 10);

      this.route.paramMap.subscribe(params => {
        this.selectedOperation = params.get('type') || '';
        this.operation = this.route.snapshot.params['operation'] || 'addition';
        console.log('selected operation:', this.operation)
      });

      console.log(`🎓 Loaded Learn Video for ${this.operation} Level ${this.level}`);
      
      const videoUrl = this.youtubeVideoMap[this.operation]?.[this.level];
      console.log('Video id:', videoUrl)
      if (videoUrl) {
        this.youtubeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
          `https://www.youtube.com/embed/${videoUrl}`
        );
        console.log('🎥 Video link:', this.youtubeUrl);
      } else {
        console.error('⚠️ Video URL not found for operation:', this.operation, 'level:', this.level);
      }
  
      // Set example
      this.example = this.exampleService.getExample(this.operation, this.level);
    });
  }
  
  get videoSrc(): string {
    return `assets/videos/${this.operation}_level${this.level}.mp4`;
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
    this.router.navigate([`/practice/$this.operation}`], {
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
    return (match && match[2].length == 11) ? match[2] : '';
  }

  youtubeVideoMap: { [operation: string]: { [level: number]: string } } = {
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


  youtubeUrl: SafeResourceUrl | null = null;
}
