import { Component, Input } from '@angular/core';

@Component({
  selector: 'kap-next-appointments',
  templateUrl: './next-appointments.component.html',
  styleUrls: ['./next-appointments.component.scss']
})
export class NextAppointmentsComponent {
  @Input() user;

  constructor() {}
}
