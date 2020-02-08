import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'kap-next-appointments',
  templateUrl: './next-appointments.component.html',
  styleUrls: ['./next-appointments.component.scss']
})
export class NextAppointmentsComponent {
  @Input() user;
  @Output() freeAppointment = new EventEmitter();

  constructor() {}
}
