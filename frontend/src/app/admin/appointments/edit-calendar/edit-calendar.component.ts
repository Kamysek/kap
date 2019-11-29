import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { switchMap } from 'rxjs/operators';
import { CalendarService } from '../../../services/calendar.service';

@Component({
  selector: 'kap-edit-calendar',
  templateUrl: './edit-calendar.component.html',
  styleUrls: ['./edit-calendar.component.scss']
})
export class EditCalendarComponent implements OnInit {
  calendar$;

  constructor(
    private route: ActivatedRoute,
    private calendarService: CalendarService
  ) {}

  ngOnInit() {
    this.calendar$ = this.route.paramMap.pipe(
      switchMap(params => this.calendarService.getCalendar(params.get('id')))
    );
    this.calendar$.subscribe(console.log);
  }
}
