import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnInit,
  Output,
  SimpleChanges
} from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map, withLatestFrom } from 'rxjs/operators';
import * as moment from 'moment';

@Component({
  selector: 'kap-week-switcher',
  templateUrl: './week-switcher.component.html',
  styleUrls: ['./week-switcher.component.scss']
})
export class WeekSwitcherComponent implements OnInit, OnChanges {
  @Input() weeks;
  @Output() open = new EventEmitter();
  weekNums = new BehaviorSubject([]);
  selectedIndex = new BehaviorSubject(0);
  selectedWeek: Observable<number>;
  selectedRage: Observable<string>;
  canGoLower: Observable<boolean>;
  canGoHigher: Observable<boolean>;
  selectedAppointments: Observable<any[]>;

  constructor() {}

  ngOnInit(): void {
    this.selectedWeek = this.selectedIndex.pipe(
      withLatestFrom(this.weekNums),
      map(([index, weeks]) => weeks[index])
    );
    this.selectedAppointments = this.selectedWeek.pipe(
      map(week => this.weeks[week])
    );
    this.canGoHigher = this.selectedIndex.pipe(
      map(index => index < this.weekNums.value.length - 1)
    );
    this.canGoLower = this.selectedIndex.pipe(map(index => index > 0));
    this.selectedRage = this.selectedWeek.pipe(
      map(week => moment(week, 'YYYYWW')),
      map(
        rangeMoment =>
          `${rangeMoment.format('D.M.')} - ${rangeMoment
            .add(4, 'days')
            .format('D.M.')}`
      )
    );
    const currentWeek = (moment().year() * 100 + moment().week()).toString(10);
    if (this.weekNums.value.includes(currentWeek)) {
      this.selectedIndex.next(this.weekNums.value.indexOf(currentWeek));
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.hasOwnProperty('weeks')) {
      this.weekNums.next(Object.keys(changes.weeks.currentValue));
      if (this.selectedIndex.value >= this.weekNums.value.length) {
        this.selectedIndex.next(0);
      } else {
        this.selectedIndex.next(this.selectedIndex.value);
      }
    }
  }

  goLower() {
    this.selectedIndex.next(this.selectedIndex.value - 1);
  }

  goHigher() {
    this.selectedIndex.next(this.selectedIndex.value + 1);
  }
}
