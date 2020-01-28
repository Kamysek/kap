import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges
} from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import * as moment from 'moment';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'kap-display-study-plan',
  templateUrl: './display-study-plan.component.html',
  styleUrls: ['./display-study-plan.component.scss']
})
export class DisplayStudyPlanComponent implements OnChanges {
  @Input() plan: any;
  @Output() newItem = new EventEmitter();
  @Output() removeItem = new EventEmitter();
  items = new BehaviorSubject([]);
  monthControl = new FormControl(null, Validators.pattern('d+'));
  nameControl = new FormControl('', Validators.required);

  constructor() {}

  ngOnChanges(changes: SimpleChanges): void {
    // console.log(changes);
    if (changes.hasOwnProperty('plan')) {
      this.items.next(
        changes.plan.currentValue.checkups.sort(item => item.daysUntil)
      );
    }
  }

  asMonths(days: number) {
    return Math.round(moment.duration(days, 'days').asMonths());
  }

  submitItem() {
    const newCheckup = {
      name: this.nameControl.value,
      daysUntil: moment.duration(this.monthControl.value, 'months').asDays()
    };
    this.newItem.emit(newCheckup);
    this.monthControl.reset(null);
    this.nameControl.reset('');
  }
}
