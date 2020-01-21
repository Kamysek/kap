import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { UserService } from '../services/user.service';
import { AppointmentsService } from '../services/appointments.service';

@Component({
  selector: 'kap-patient',
  templateUrl: './patient.component.html',
  styleUrls: ['./patient.component.scss']
})
export class PatientComponent implements OnInit {
  slots$;
  patient$;

  constructor(
    private authService: AuthService,
    private userService: UserService,
    private appointmentsService: AppointmentsService
  ) {}

  ngOnInit() {
    // this.calendars$ = this.calendarService.getAppointments();
    this.slots$ = this.appointmentsService.getDays();
    this.patient$ = this.userService.getOwnDetails();
  }

  async takeAppointment(list) {
    await this.appointmentsService.bookSlot({ list }).toPromise();
  }

  logout() {
    this.authService.logout();
  }
}
