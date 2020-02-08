import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { UserService } from '../services/user.service';
import { AppointmentsService } from '../services/appointments.service';
import { BehaviorSubject } from 'rxjs';
import * as moment from 'moment';
import { filter, map, switchMap, tap } from 'rxjs/operators';
import { MatDialog } from '@angular/material/dialog';
import { CollectCommentDialogComponent } from './collect-comment-dialog/collect-comment-dialog.component';

@Component({
  selector: 'kap-patient',
  templateUrl: './patient.component.html',
  styleUrls: ['./patient.component.scss']
})
export class PatientComponent implements OnInit {
  slots$;
  patient$;
  appointmentConfig = new BehaviorSubject({
    plus: 7,
    minus: 7,
    date: moment().add(2, 'week')
  });
  canLoadMore = this.appointmentConfig.pipe(
    map(config => config.minus > config.date.diff(moment(), 'days'))
  );

  constructor(
    private authService: AuthService,
    private userService: UserService,
    private appointmentsService: AppointmentsService,
    private dialog: MatDialog
  ) {}

  ngOnInit() {
    this.slots$ = this.appointmentConfig.pipe(
      switchMap(config => this.appointmentsService.getDays(config))
    );
    this.patient$ = this.userService.getOwnDetails().pipe(
      filter(user => !!user),
      tap(details =>
        this.appointmentConfig.next({
          ...this.appointmentConfig.value,
          date: moment(details.nextCheckup)
        })
      )
    );
  }

  async takeAppointment(slot) {
    const commentPatient = await this.dialog
      .open(CollectCommentDialogComponent, { data: slot })
      .afterClosed()
      .toPromise();
    if (commentPatient) {
      await this.appointmentsService
        .bookSlot(
          { input: { commentPatient, appointmentList: slot.appointments } },
          this.appointmentConfig.value
        )
        .toPromise();
    }
  }

  loadMoreAppointments() {
    this.appointmentConfig.next({
      ...this.appointmentConfig.value,
      minus: this.appointmentConfig.value.minus + 7
    });
  }

  async freeAppointment(appointment) {
    await this.appointmentsService
      .updateAppointment({
        id: appointment.id,
        taken: false
      })
      .toPromise();
  }

  logout() {
    this.authService.logout();
  }
}
