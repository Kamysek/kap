import { Component, OnInit } from '@angular/core';
import { CalendarService } from '../services/calendar.service';

@Component({
  selector: 'kap-patient',
  templateUrl: './patient.component.html',
  styleUrls: ['./patient.component.scss']
})
export class PatientComponent implements OnInit {
  calendars$;

  constructor(private calendarService: CalendarService) {}

  ngOnInit() {
    this.calendars$ = this.calendarService.getAppointments();
  }

  takeAppointment(id) {
    console.log(id);
    this.calendarService.takeAppointment({ id });
  }
}
