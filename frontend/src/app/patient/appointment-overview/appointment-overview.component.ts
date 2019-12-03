import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Input,
  Output
} from '@angular/core';

@Component({
  selector: 'kap-appointment-overview',
  templateUrl: './appointment-overview.component.html',
  styleUrls: ['./appointment-overview.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppointmentOverviewComponent {
  @Input() calendars;
  @Output() takeAppointment = new EventEmitter();

  constructor() {}
}
