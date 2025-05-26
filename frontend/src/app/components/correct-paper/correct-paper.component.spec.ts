import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CorrectPaperComponent } from './correct-paper.component';

describe('CorrectPaperComponent', () => {
  let component: CorrectPaperComponent;
  let fixture: ComponentFixture<CorrectPaperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CorrectPaperComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CorrectPaperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
