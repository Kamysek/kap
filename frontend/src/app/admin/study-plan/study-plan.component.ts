import { Component, OnDestroy, OnInit } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { MatDialog } from '@angular/material';
import { map, startWith, takeUntil, withLatestFrom } from 'rxjs/operators';
import { FormControl } from '@angular/forms';

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

  constructor(private route: ActivatedRoute, private dialog: MatDialog) {}

  ngOnInit() {
    this.studyPlans = this.route.data.pipe(map(data => data.plans));
    this.studyPlans
      .pipe(takeUntil(this.destroyed))
      .subscribe(plans => this.planControl.reset(plans[0].id));
    this.selectedPlan = this.planControl.valueChanges.pipe(
      startWith(this.planControl.value),
      withLatestFrom(this.studyPlans),
      map(([id, plans]) => plans.find(plan => plan.id === id))
    );
  }

  ngOnDestroy(): void {
    this.destroyed.complete();
  }
}
