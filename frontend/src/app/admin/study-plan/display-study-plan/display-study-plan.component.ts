import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'kap-display-study-plan',
  templateUrl: './display-study-plan.component.html',
  styleUrls: ['./display-study-plan.component.scss']
})
export class DisplayStudyPlanComponent implements OnChanges {
  @Input() plan: any;
  items = new BehaviorSubject([]);

  constructor() {}

  ngOnChanges(changes: SimpleChanges): void {
    // console.log(changes);
    if (changes.hasOwnProperty('plan')) {
      this.items.next(
        changes.plan.currentValue.checkups.sort(item => item.order)
      );
    }
  }
}
