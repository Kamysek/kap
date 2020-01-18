import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DisplayStudyPlanComponent } from './display-study-plan.component';

describe('DisplayStudyPlanComponent', () => {
  let component: DisplayStudyPlanComponent;
  let fixture: ComponentFixture<DisplayStudyPlanComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [DisplayStudyPlanComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DisplayStudyPlanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
