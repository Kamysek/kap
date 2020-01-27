import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { AppointmentsService } from '../../services/appointments.service';
import { map } from 'rxjs/operators';
import * as moment from 'moment';

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
    private appointmentsService: AppointmentsService
  ) {}

  ngOnInit() {
    this.appointments$ = this.appointmentsService.getCurrentWeek();
    this.days$ = this.appointments$.pipe(
      map(appointments =>
        Object.keys(appointments).map(dayNum =>
          Object.assign({}, { dayNum, dayMoment: moment(dayNum, 'YYYDD') })
        )
      )
    );
  }

  logout() {
    this.authService.logout();
  }
}
