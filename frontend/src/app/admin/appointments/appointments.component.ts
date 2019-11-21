import {Component, OnInit} from '@angular/core';
import {MatDialog} from '@angular/material';
import {NewCalendarDialogComponent} from './new-calendar-dialog/new-calendar-dialog.component';
import {CalendarService} from '../../services/calendar.service';

@Component({
  selector: 'kap-appointments',
  templateUrl: './appointments.component.html',
  styleUrls: ['./appointments.component.scss']
})
export class AppointmentsComponent implements OnInit {

  constructor(private dialog: MatDialog, private calendarService:CalendarService) {
  }

  ngOnInit() {
  }

  createCalendar() {
    this.dialog.open(NewCalendarDialogComponent).afterClosed().subscribe(res => {
      if (!res) {
        return;
      }
      this.calendarService.createNew(res);
    });
  }
}
