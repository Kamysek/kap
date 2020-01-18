import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { AppointmentsService } from '../../services/appointments.service';

@Component({
  selector: 'kap-lab-overview',
  templateUrl: './lab-overview.component.html',
  styleUrls: ['./lab-overview.component.scss']
})
export class LabOverviewComponent implements OnInit {
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
