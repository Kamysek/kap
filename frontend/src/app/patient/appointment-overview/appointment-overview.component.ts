import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges
} from '@angular/core';
import * as moment from 'moment';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'kap-appointment-overview',
  templateUrl: './appointment-overview.component.html',
  styleUrls: ['./appointment-overview.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppointmentOverviewComponent implements OnChanges {
  @Input() appointments;
  @Input() canLoadMore;
  @Output() takeAppointment = new EventEmitter();
  @Output() loadMore = new EventEmitter();
  days = new BehaviorSubject([]);

  constructor() {}

  ngOnChanges(changes: SimpleChanges): void {
    if (
      changes.hasOwnProperty('appointments') &&
      changes.appointments.currentValue
    ) {
      this.days.next(
        Object.keys(changes.appointments.currentValue).map(day =>
          Object.assign(
            {},
            {
              slots: changes.appointments.currentValue[day],
              dayMoment: moment(day, 'YYYYDDDD')
            }
          )
        )
      );
    }
  }
}
