import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadAnswersComponent } from './upload-answers.component';

describe('UploadAnswersComponent', () => {
  let component: UploadAnswersComponent;
  let fixture: ComponentFixture<UploadAnswersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UploadAnswersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UploadAnswersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
