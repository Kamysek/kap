import { CalendarService } from '../../services/calendar.service';
import { first } from 'rxjs/operators';
import { Observable } from 'rxjs';
import {
  ActivatedRouteSnapshot,
  Resolve,
  RouterStateSnapshot
} from '@angular/router';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class CalendarResolver implements Resolve<any> {
  constructor(private calendarService: CalendarService) {}

  resolve(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<any> | Promise<any> | any {
    return this.calendarService
      .getCalendar(route.paramMap.get('id'))
      .pipe(first());
  }
}