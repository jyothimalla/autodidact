import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TimeQuestionComponent } from './time-questions.component';

describe('TimeQuestionComponent', () => {
  let component: TimeQuestionComponent;
  let fixture: ComponentFixture<TimeQuestionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TimeQuestionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TimeQuestionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
