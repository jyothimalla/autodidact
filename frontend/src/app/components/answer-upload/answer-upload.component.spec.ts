import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnswerUploadComponent } from './answer-upload.component';

describe('AnswerUploadComponent', () => {
  let component: AnswerUploadComponent;
  let fixture: ComponentFixture<AnswerUploadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AnswerUploadComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AnswerUploadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
