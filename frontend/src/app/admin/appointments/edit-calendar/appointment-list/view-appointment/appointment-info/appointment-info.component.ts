import { Component, Input } from '@angular/core';

@Component({
  selector: 'kap-appointment-info',
  templateUrl: './appointment-info.component.html',
  styleUrls: ['./appointment-info.component.scss']
})
export class AppointmentInfoComponent {
  @Input() appointment;
}
