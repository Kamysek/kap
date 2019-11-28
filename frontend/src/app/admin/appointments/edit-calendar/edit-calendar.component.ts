import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Component({
  selector: 'kap-edit-calendar',
  templateUrl: './edit-calendar.component.html',
  styleUrls: ['./edit-calendar.component.scss']
})
export class EditCalendarComponent implements OnInit {
  calendar$: Observable<any>;
  title$: Observable<string>;

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.calendar$ = this.route.data.pipe(map(data => data.calendar));
    this.title$ = this.calendar$.pipe(
      map(calendar => `${calendar.name} (${calendar.id})`)
    );
  }
}
