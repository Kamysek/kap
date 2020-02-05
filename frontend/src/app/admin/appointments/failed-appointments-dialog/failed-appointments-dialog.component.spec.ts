import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FailedAppointmentsDialogComponent } from './failed-appointments-dialog.component';

describe('FailedAppointmentsDialogComponent', () => {
  let component: FailedAppointmentsDialogComponent;
  let fixture: ComponentFixture<FailedAppointmentsDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [FailedAppointmentsDialogComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FailedAppointmentsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
