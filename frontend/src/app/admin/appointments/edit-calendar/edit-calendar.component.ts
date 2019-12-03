import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { map, startWith, switchMap } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { CalendarService } from '../../../services/calendar.service';

@Component({
  selector: 'kap-edit-calendar',
  templateUrl: './edit-calendar.component.html',
  styleUrls: ['./edit-calendar.component.scss']
})
export class EditCalendarComponent implements OnInit {
  calendar$: Observable<any>;
  title$: Observable<string>;

  constructor(
    private route: ActivatedRoute,
    private calendarService: CalendarService
  ) {}

  ngOnInit() {
    this.calendar$ = this.route.data.pipe(
      map(data => data.calendar),
      switchMap(calendar =>
        this.calendarService.getCalendar(calendar.id).pipe(startWith(calendar))
      )
    );
    this.title$ = this.calendar$.pipe(
      map(calendar => `${calendar.name} (${calendar.id})`)
    );
  }
}
