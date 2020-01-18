import { first } from 'rxjs/operators';
import { Observable } from 'rxjs';
import {
  ActivatedRouteSnapshot,
  Resolve,
  RouterStateSnapshot
} from '@angular/router';
import { Injectable } from '@angular/core';
import { StudyPlanService } from '../../services/study-plan.service';

@Injectable({ providedIn: 'root' })
export class PlanResolver implements Resolve<any> {
  constructor(private planService: StudyPlanService) {}

  resolve(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<any> | Promise<any> | any {
    return this.planService.getPlans().pipe(first());
  }
}
