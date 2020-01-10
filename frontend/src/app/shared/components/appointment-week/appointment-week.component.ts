import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import * as moment from 'moment';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'kap-appointment-week',
  templateUrl: './appointment-week.component.html',
  styleUrls: ['./appointment-week.component.scss']
})
export class AppointmentWeekComponent implements OnChanges {
  @Input() appointments;
  @Input() week;
  days = new BehaviorSubject([]);
  times = [];
  filler = [];

  constructor() {
    const morningMoment = moment()
      .startOf('day')
      .add(8, 'hours');
    for (let i = 0; i < 8 * 4; i++) {
      this.times.push(morningMoment.format('HH:mm'));
      morningMoment.add(15, 'minutes');
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.hasOwnProperty('week')) {
      const weekMoment = moment(changes.week.currentValue, 'YYYYWW');
      const days = [];
      for (let i = 0; i < 5; i++) {
        days.push(weekMoment.format('dddd D.M.'));
        weekMoment.add(1, 'day');
      }
      this.days.next(days);
    }
    if (changes.hasOwnProperty('appointments')) {
      this.filler = [];
      for (
        let i = 0;
        i < 5 * 8 * 4 + 1 - changes.appointments.currentValue.length * 3;
        i++
      ) {
        this.filler.push(i);
      }
    }
  }
}
