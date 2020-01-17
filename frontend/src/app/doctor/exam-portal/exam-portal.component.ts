import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { AppointmentsService } from '../../services/appointments.service';

@Component({
  selector: 'kap-exam-portal',
  templateUrl: './exam-portal.component.html',
  styleUrls: ['./exam-portal.component.scss']
})
export class ExamPortalComponent implements OnInit {
  appointments$;

  constructor(
    private authService: AuthService,
    private appointmentsService: AppointmentsService
  ) {}

  ngOnInit() {
    this.appointments$ = this.appointmentsService.getCurrentWeek();
  }

  logout() {
    this.authService.logout();
  }
}
