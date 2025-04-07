import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubtractionComponent } from './subtraction.component';

describe('SubtractionComponent', () => {
  let component: SubtractionComponent;
  let fixture: ComponentFixture<SubtractionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SubtractionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SubtractionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
