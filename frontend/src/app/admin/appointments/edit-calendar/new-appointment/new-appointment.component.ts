import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Input,
  Output
} from '@angular/core';
import { CalendarService } from '../../../../services/calendar.service';

@Component({
  selector: 'kap-new-appointment',
  templateUrl: './new-appointment.component.html',
  styleUrls: ['./new-appointment.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class NewAppointmentComponent {
  @Input() calendarId;
  @Output() done = new EventEmitter();

  constructor(private calendarService: CalendarService) {}

  saveAppointment(data) {
    console.log(data);
    this.calendarService.addAppointment({ ...data, calendar: this.calendarId });
    this.done.emit();
  }
}
