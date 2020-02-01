import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { first, map, startWith } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { MatDialog } from '@angular/material';
import { AddAppointmentsDialogComponent } from './add-appointments-dialog/add-appointments-dialog.component';
import { EditAppointmentDialogComponent } from './edit-appointment-dialog/edit-appointment-dialog.component';
import { AppointmentsService } from '../../services/appointments.service';

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

  openAppointmentsDialog() {
    this.dialog.open(AddAppointmentsDialogComponent);
  }

  editAppointment(appointment) {
    this.dialog
      .open(EditAppointmentDialogComponent, { data: appointment })
      .afterClosed()
      .pipe(first())
      .subscribe(async patch => {
        if (!!patch) {
          await this.appointmentsService.updateAppointment(patch).toPromise();
        }
      });
  }
}
