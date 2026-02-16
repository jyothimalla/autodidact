import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { of } from 'rxjs';

import { LearnComponent } from './learn.component';
import { ExampleService } from '../../services/example.service';
import { QuizService } from '../../services/quiz.service';

describe('LearnComponent', () => {
  let component: LearnComponent;
  let fixture: ComponentFixture<LearnComponent>;

  beforeEach(async () => {
    const activatedRouteStub = {
      paramMap: of(convertToParamMap({ operation: 'addition' })),
      queryParams: of({ level: '0', username: 'tester', user_id: '1' })
    };

    await TestBed.configureTestingModule({
      imports: [LearnComponent],
      providers: [
        provideRouter([]),
        { provide: ActivatedRoute, useValue: activatedRouteStub },
        {
          provide: ExampleService,
          useValue: { getExample: () => ({ question: '1 + 1', answer: 2 }) }
        },
        {
          provide: QuizService,
          useValue: { getUserProgressByOperation: () => of({ ninja_stars: 0, progress: [] }) }
        }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LearnComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should build a valid practice route', () => {
    spyOn((component as any).router, 'navigate');
    component.goToPractice();
    expect((component as any).router.navigate).toHaveBeenCalledWith(['/practice/addition'], jasmine.anything());
  });
});
