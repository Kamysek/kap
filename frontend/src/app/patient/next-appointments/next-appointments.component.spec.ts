import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NextAppointmentsComponent } from './next-appointments.component';

describe('NextAppointmentsComponent', () => {
  let component: NextAppointmentsComponent;
  let fixture: ComponentFixture<NextAppointmentsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [NextAppointmentsComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NextAppointmentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
