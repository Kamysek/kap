import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddAppointmentsDialogComponent } from './add-appointments-dialog.component';

describe('AddAppointmentsDialogComponent', () => {
  let component: AddAppointmentsDialogComponent;
  let fixture: ComponentFixture<AddAppointmentsDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [AddAppointmentsDialogComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddAppointmentsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
