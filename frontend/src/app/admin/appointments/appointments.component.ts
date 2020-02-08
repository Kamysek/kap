import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { first, map, startWith } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { AddAppointmentsDialogComponent } from './add-appointments-dialog/add-appointments-dialog.component';
import { EditAppointmentDialogComponent } from './edit-appointment-dialog/edit-appointment-dialog.component';
import { AppointmentsService } from '../../services/appointments.service';
import { FailedAppointmentsDialogComponent } from './failed-appointments-dialog/failed-appointments-dialog.component';

@Component({
  selector: 'kap-appointments',
  templateUrl: './appointments.component.html',
  styleUrls: ['./appointments.component.scss']
})
export class AppointmentsComponent implements OnInit {
  appointments: Observable<any>;
  hasAppointments: Observable<boolean>;

  constructor(
    private route: ActivatedRoute,
    private dialog: MatDialog,
    private appointmentsService: AppointmentsService
  ) {}

  ngOnInit() {
    this.appointments = this.appointmentsService
      .getWeeks()
      .pipe(startWith(this.route.snapshot.data.appointments));
    this.hasAppointments = this.appointments.pipe(
      map(appointments => !!Object.keys(appointments).length)
    );
  }

  async openAppointmentsDialog() {
    const failedAppointments = await this.dialog
      .open(AddAppointmentsDialogComponent)
      .afterClosed()
      .toPromise();
    console.log(failedAppointments);
    console.log('Dialog closed');
    if (failedAppointments && failedAppointments.length) {
      this.dialog.open(FailedAppointmentsDialogComponent, {
        data: { failedAppointments }
      });
    }
  }

  editAppointment(appointment) {
    this.dialog
      .open(EditAppointmentDialogComponent, { data: appointment })
      .afterClosed()
      .pipe(first())
      .subscribe(async patch => {
        if (!!patch) {
          if (typeof patch === 'object') {
            await this.appointmentsService.updateAppointment(patch).toPromise();
          } else if (patch === 'free') {
            await this.appointmentsService
              .updateAppointment({ id: appointment.id, taken: false })
              .toPromise();
          }
        }
      });
  }
}
