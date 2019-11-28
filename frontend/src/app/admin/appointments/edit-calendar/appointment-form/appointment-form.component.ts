import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Input,
  OnInit,
  Output
} from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'kap-appointment-form',
  templateUrl: './appointment-form.component.html',
  styleUrls: ['./appointment-form.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppointmentFormComponent implements OnInit {
  @Input() appointment;
  @Output() save = new EventEmitter();
  @Output() cancel = new EventEmitter();
  appointmentForm: FormGroup;

  constructor(fb: FormBuilder) {
    this.appointmentForm = fb.group({
      appointmentStart: [null, Validators.required],
      appointmentStartTime: [
        ' ',
        Validators.pattern('^([01]\\d|2[0-3]):([0-5]\\d)$')
      ],
      title: ['', Validators.required]
    });
  }

  ngOnInit() {
    if (this.appointment) {
      console.log(this.appointment);
      const appointmentStartTime = this.appointment.appointmentStart.format(
        'HH:mm'
      );
      this.appointment.appointmentStart.startOf('day');
      this.appointmentForm.reset({ ...this.appointment, appointmentStartTime });
    }
  }

  submit() {
    const value = this.appointmentForm.value;
    this.appointmentForm.disable();
    const startTime = value.appointmentStartTime.split(':');
    delete value.appointmentStartTime;
    value.appointmentStart.hours(startTime[0]).minutes(startTime[1]);
    value.appointmentEnd = value.appointmentStart
      .clone()
      .add(1, 'hour')
      .toDate();
    value.appointmentStart = value.appointmentStart.toDate();
    this.save.emit(value);
  }
}
