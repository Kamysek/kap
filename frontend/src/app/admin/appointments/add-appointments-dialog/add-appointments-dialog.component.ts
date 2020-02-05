import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, Validators } from '@angular/forms';
import * as moment from 'moment';
import 'moment-recur-ts';
import 'moment-timezone';
import { map, startWith } from 'rxjs/operators';
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

  currentWeekMoment = moment()
    .tz('Europe/Berlin')
    .startOf('week');
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
      startWith(this.appointmentsForm.value),
      map(({ appointments, repeat }) => appointments.length * repeat)
    );
    this.lastAppointment = this.appointmentsForm.valueChanges.pipe(
      startWith(this.appointmentsForm.value),
      map(({ appointments, repeat }) =>
        moment(this.currentWeekMoment)
          .isoWeekday(Math.max(...appointments.map(appt => appt.day)))
          .add(repeat, 'weeks')
      )
    );
  }

  addAppointment() {
    let newTime = '08:00';
    let newDay = 1;
    if (this.appointments.length) {
      const lastAppointment = this.appointments.controls[
        this.appointments.length - 1
      ];
      newTime = moment(lastAppointment.get('time').value, 'HH:mm')
        .add(30, 'minutes')
        .format('HH:mm');
      newDay = lastAppointment.get('day').value;
    }
    this.appointments.push(
      this.fb.group({
        day: [newDay, Validators.pattern('[1-5]')],
        time: [
          newTime,
          Validators.pattern('(08|09|10|11|12|13|14|15):(00|15|30|45)')
        ]
      })
    );
  }

  deleteAppointment(index) {
    this.appointments.removeAt(index);
  }

  async saveAppointments() {
    const value = this.appointmentsForm.value;
    this.appointmentsForm.disable();
    const appointments = value.appointments.reduce((acc, curr) => {
      const firstMoment = moment(this.currentWeekMoment)
        .isoWeekday(curr.day)
        .hour(parseInt(curr.time.split(':')[0], 10))
        .minute(parseInt(curr.time.split(':')[1], 10));
      return acc.concat(
        ...[...Array(value.repeat).keys()].map(week =>
          Object.assign(
            {},
            {
              title: 'Appointment',
              appointmentStart: moment(firstMoment).add(week, 'weeks'),
              appointmentEnd: moment(firstMoment)
                .add(week, 'weeks')
                .add(30, 'minutes')
            }
          )
        )
      );
    }, []);
    const failed = await this.appointmentsService
      .createAppointments(appointments)
      .toPromise();
    this.dialog.close(failed);
  }
}
