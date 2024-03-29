import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import * as moment from 'moment';

@Component({
  selector: 'kap-edit-appointment-dialog',
  templateUrl: './edit-appointment-dialog.component.html',
  styleUrls: ['./edit-appointment-dialog.component.scss'],
})
export class EditAppointmentDialogComponent implements OnInit {
  appointmentForm: FormGroup;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialog: MatDialogRef<EditAppointmentDialogComponent>,
    fb: FormBuilder
  ) {
    this.appointmentForm = fb.group({
      startDate: [null, Validators.required],
      startTime: ['', Validators.pattern('(0|1)[0-5]|9|8:(00|15|30|45)')],
      title: ['', Validators.required],
      taken: {
        value: false,
        validators: [Validators.required],
        disabled: true,
      },
      commentDoctor: [''],
      commentPatient: [''],
    });
  }

  ngOnInit() {
    const {
      title,
      taken,
      commentDoctor,
      commentPatient,
      startMoment,
    } = this.data;
    this.appointmentForm.setValue({
      startDate: startMoment,
      startTime: startMoment.format('HH:mm'),
      title,
      taken,
      commentDoctor,
      commentPatient,
    });
    if (moment() > startMoment) {
      this.appointmentForm.get('startDate').disable();
      this.appointmentForm.get('startTime').disable();
    }
    if (this.appointmentForm.get('taken').value) {
      this.appointmentForm.get('taken').disable();
    }
  }

  submit() {
    this.appointmentForm.get('startDate').enable();
    this.appointmentForm.get('startTime').enable();
    const formValue = this.appointmentForm.value;
    const startMoment = formValue.startDate
      .hour(parseInt(formValue.startTime.split(':')[0], 10))
      .minute(parseInt(formValue.startTime.split(':')[1], 10));
    const takenEnabled = this.appointmentForm.get('taken').enabled;
    this.appointmentForm.disable();
    const patch = {
      id: this.data.id,
      title: formValue.title,
      commentDoctor: formValue.commentDoctor,
      commentPatient: formValue.commentPatient,
      appointmentStart: moment(startMoment).toDate(),
      appointmentEnd: moment(startMoment).add(30, 'minutes').toDate(),
      taken: takenEnabled ? formValue.taken : true,
    };
    this.dialog.close(patch);
  }

  freeAppointment() {
    this.dialog.close('free');
  }
}
