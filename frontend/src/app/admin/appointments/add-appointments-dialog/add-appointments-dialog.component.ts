import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, Validators } from '@angular/forms';
import * as moment from 'moment';
import 'moment-recur-ts';
import { map } from 'rxjs/operators';
import { MatDialogRef } from '@angular/material';
import { AppointmentsService } from '../../../services/appointments.service';

@Component({
  selector: 'kap-add-appointments-dialog',
  templateUrl: './add-appointments-dialog.component.html',
  styleUrls: ['./add-appointments-dialog.component.scss']
})
export class AddAppointmentsDialogComponent implements OnInit {
  appointmentsForm = this.fb.group({
    appointments: this.fb.array([]),
    repeat: [1, Validators.min(1)]
  });

  currentWeekMoment = moment().startOf('week');
  lastAppointment;
  appointmentNum;

  constructor(
    private fb: FormBuilder,
    private dialog: MatDialogRef<AddAppointmentsDialogComponent>,
    private appointmentsService: AppointmentsService
  ) {}

  get appointments() {
    return this.appointmentsForm.get('appointments') as FormArray;
  }

  ngOnInit() {
    this.addAppointment();
    this.appointments.valueChanges.subscribe(console.log);
    this.appointments.valueChanges.subscribe(appointments => {
      const maxDay = Math.max(...appointments.map(appt => appt.day));
    });
    this.appointmentNum = this.appointmentsForm.valueChanges.pipe(
      map(({ appointments, repeat }) => appointments.length * repeat)
    );
    this.lastAppointment = this.appointmentsForm.valueChanges.pipe(
      map(({ appointments, repeat }) =>
        moment(this.currentWeekMoment)
          .isoWeekday(Math.max(...appointments.map(appt => appt.day)))
          .add(repeat, 'weeks')
      )
    );
  }

  addAppointment() {
    this.appointments.push(
      this.fb.group({
        day: [1, Validators.pattern('[1-5]')],
        time: ['08:00', Validators.pattern('(0|1)[0-5]|9|8:(00|15|30|45)')]
      })
    );
  }

  deleteAppointment(index) {
    this.appointments.removeAt(index);
  }

  async saveAppointments() {
    const value = this.appointmentsForm.value;
    this.appointmentsForm.disable();
    const appointments = value.appointments.reduce(
      (acc, curr) =>
        acc.concat(
          ...moment(this.currentWeekMoment)
            .isoWeekday(curr.day)
            .recur()
            .every(1)
            .weeks()
            .next(value.repeat)
            .map(date =>
              Object.assign(
                {},
                {
                  title: 'Appointment',
                  appointmentStart: moment(date)
                    .hour(parseInt(curr.time.split(':')[0], 10))
                    .minute(parseInt(curr.time.split(':')[1], 10)),
                  appointmentEnd: moment(date)
                    .hour(parseInt(curr.time.split(':')[0], 10))
                    .minute(parseInt(curr.time.split(':')[1], 10))
                    .add(45, 'minutes')
                }
              )
            )
        ),
      []
    );
    console.log(JSON.stringify(appointments));
    await this.appointmentsService.createAppointments(appointments);
    this.dialog.close(true);
  }
}
