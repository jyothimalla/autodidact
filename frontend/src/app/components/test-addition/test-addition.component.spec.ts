import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestAdditionComponent } from './test-addition.component';

describe('TestAdditionComponent', () => {
  let component: TestAdditionComponent;
  let fixture: ComponentFixture<TestAdditionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestAdditionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TestAdditionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
