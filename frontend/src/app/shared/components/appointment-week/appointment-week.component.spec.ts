import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AppointmentWeekComponent } from './appointment-week.component';

describe('AppointmentWeeksComponent', () => {
  let component: AppointmentWeekComponent;
  let fixture: ComponentFixture<AppointmentWeekComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [AppointmentWeekComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AppointmentWeekComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
