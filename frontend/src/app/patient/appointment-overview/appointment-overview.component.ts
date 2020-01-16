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
  @Output() takeAppointment = new EventEmitter();
  days = new BehaviorSubject([]);

  constructor() {}

  ngOnChanges(changes: SimpleChanges): void {
    console.log(changes);
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
