import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import * as moment from 'moment';

@Component({
  selector: 'kap-appointment-overview',
  templateUrl: './appointment-overview.component.html',
  styleUrls: ['./appointment-overview.component.scss']
})
export class AppointmentOverviewComponent implements OnChanges {
  @Input() appointments;
  days = new BehaviorSubject([]);

  constructor() {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.hasOwnProperty('appointments')) {
      console.log(changes.appointments.currentValue);
      this.days.next(
        Object.keys(changes.appointments.currentValue).map(day =>
          Object.assign(
            {},
            {
              appointments: changes.appointments.currentValue[day],
              dayMoment: moment(day, 'YYYYDDDD')
            }
          )
        )
      );
    }
  }
}
