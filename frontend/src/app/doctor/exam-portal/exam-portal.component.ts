import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { AppointmentsService } from '../../services/appointments.service';
import { first, map } from 'rxjs/operators';
import * as moment from 'moment';
import { MatDialog } from '@angular/material';
import { MakeAppointmentDialogComponent } from './make-appointment-dialog/make-appointment-dialog.component';

@Component({
  selector: 'kap-exam-portal',
  templateUrl: './exam-portal.component.html',
  styleUrls: ['./exam-portal.component.scss']
})
export class ExamPortalComponent implements OnInit {
  appointments$;
  days$;

  constructor(
    private authService: AuthService,
    private dialog: MatDialog,
    private appointmentsService: AppointmentsService
  ) {}

  ngOnInit() {
    this.appointments$ = this.appointmentsService.getCurrentWeek();
    this.days$ = this.appointments$.pipe(
      map(appointments =>
        Object.keys(appointments).map(dayNum =>
          Object.assign({}, { dayNum, dayMoment: moment(dayNum, 'YYYYDD') })
        )
      )
    );
  }

  reportNoShow(id) {}

  async makeNewAppointment(user) {
    const slots = await this.appointmentsService
      .getDays({ minus: 7, plus: 7, userId: user.id })
      .pipe(first())
      .toPromise();
    const choice = await this.dialog
      .open(MakeAppointmentDialogComponent, {
        data: { user, slots }
        // minHeight: '70vh',
        // minWidth: '80vw'
      })
      .afterClosed()
      .toPromise();
  }

  logout() {
    this.authService.logout();
  }
}
