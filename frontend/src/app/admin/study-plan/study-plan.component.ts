import { Component, OnDestroy, OnInit } from '@angular/core';
import { combineLatest, Observable, Subject } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { map, startWith, takeUntil } from 'rxjs/operators';
import { FormControl } from '@angular/forms';
import { StudyPlanService } from '../../services/study-plan.service';

@Component({
  selector: 'kap-study-plan',
  templateUrl: './study-plan.component.html',
  styleUrls: ['./study-plan.component.scss']
})
export class StudyPlanComponent implements OnInit, OnDestroy {
  studyPlans: Observable<any>;
  selectedPlan: Observable<any>;
  planControl = new FormControl();
  destroyed = new Subject();

  constructor(
    private route: ActivatedRoute,
    private studyPlanService: StudyPlanService
  ) {}

  ngOnInit() {
    this.studyPlans = this.studyPlanService
      .getPlans()
      .pipe(startWith(this.route.snapshot.data.plans));
    this.studyPlans
      .pipe(takeUntil(this.destroyed))
      .subscribe(plans => this.planControl.reset(plans[0].id));
    this.selectedPlan = combineLatest(
      this.studyPlans,
      this.planControl.valueChanges.pipe(startWith(this.planControl.value))
    ).pipe(map(([plans, id]) => plans.find(plan => plan.id === id)));
  }

  async newCheckup(input) {
    await this.studyPlanService
      .createCheckup({ ...input, studyId: this.planControl.value })
      .toPromise();
  }

  async deleteCheckup(id) {
    await this.studyPlanService.deleteCheckup({ id }).toPromise();
  }

  ngOnDestroy(): void {
    this.destroyed.complete();
  }
}
