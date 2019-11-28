import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

@Component({
  selector: 'kap-appointment-list',
  templateUrl: './appointment-list.component.html',
  styleUrls: ['./appointment-list.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppointmentListComponent {
  @Input() calendar;
  showNewAppointment = false;
}
