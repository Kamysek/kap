import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { UserService } from '../services/user.service';
import { AppointmentsService } from '../services/appointments.service';
import { BehaviorSubject } from 'rxjs';
import * as moment from 'moment';
import { map, switchMap } from 'rxjs/operators';

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
    private appointmentsService: AppointmentsService
  ) {}

  ngOnInit() {
    this.slots$ = this.appointmentConfig.pipe(
      switchMap(config => this.appointmentsService.getDays(config))
    );
    this.patient$ = this.userService.getOwnDetails();
  }

  async takeAppointment(list) {
    await this.appointmentsService
      .bookSlot({ list }, this.appointmentConfig.value)
      .toPromise();
  }

  loadMoreAppointments() {
    this.appointmentConfig.next({
      ...this.appointmentConfig.value,
      minus: this.appointmentConfig.value.minus + 7
    });
  }

  logout() {
    this.authService.logout();
  }
}
