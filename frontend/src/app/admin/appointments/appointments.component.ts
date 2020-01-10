import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { MatDialog } from '@angular/material';
import { AddAppointmentsDialogComponent } from './add-appointments-dialog/add-appointments-dialog.component';

@Component({
  selector: 'kap-appointments',
  templateUrl: './appointments.component.html',
  styleUrls: ['./appointments.component.scss']
})
export class AppointmentsComponent implements OnInit {
  appointments: Observable<any>;

  constructor(private route: ActivatedRoute, private dialog: MatDialog) {}

  ngOnInit() {
    this.appointments = this.route.data.pipe(map(data => data.appointments));
  }

  openAppointmentsDialog() {
    this.dialog.open(AddAppointmentsDialogComponent);
  }
}
