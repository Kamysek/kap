import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material';

@Component({
  selector: 'kap-failed-appointments-dialog',
  templateUrl: './failed-appointments-dialog.component.html',
  styleUrls: ['./failed-appointments-dialog.component.scss']
})
export class FailedAppointmentsDialogComponent implements OnInit {
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { failedAppointments: any[] }
  ) {}

  ngOnInit() {}
}
