import { first } from 'rxjs/operators';
import { Observable } from 'rxjs';
import {
  ActivatedRouteSnapshot,
  Resolve,
  RouterStateSnapshot
} from '@angular/router';
import { Injectable } from '@angular/core';
import { AppointmentsService } from '../../services/appointments.service';

@Injectable({ providedIn: 'root' })
export class AppointmentResolver implements Resolve<any> {
  constructor(private appointmentsService: AppointmentsService) {}

  resolve(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<any> | Promise<any> | any {
    return this.appointmentsService.getWeeks().pipe(first());
  }
}
