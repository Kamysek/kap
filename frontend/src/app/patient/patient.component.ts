import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { UserService } from '../services/user.service';

@Component({
  selector: 'kap-patient',
  templateUrl: './patient.component.html',
  styleUrls: ['./patient.component.scss']
})
export class PatientComponent implements OnInit {
  calendars$;
  patient$;

  constructor(
    private authService: AuthService,
    private userService: UserService
  ) {}

  ngOnInit() {
    // this.calendars$ = this.calendarService.getAppointments();
    this.patient$ = this.userService.getOwnDetails();
  }

  takeAppointment(id) {
    console.log(id);
    // this.calendarService.takeAppointment({ id });
  }

  logout() {
    this.authService.logout();
  }
}
