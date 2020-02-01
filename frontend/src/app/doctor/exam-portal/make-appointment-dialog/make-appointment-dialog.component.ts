import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material';
import * as moment from 'moment';

@Component({
  selector: 'kap-make-appointment-dialog',
  templateUrl: './make-appointment-dialog.component.html',
  styleUrls: ['./make-appointment-dialog.component.scss']
})
export class MakeAppointmentDialogComponent implements OnInit {
  days;

  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {}

  ngOnInit() {
    this.days = Object.keys(this.data.slots).map(day =>
      Object.assign(
        {},
        {
          slots: this.data.slots[day],
          dayMoment: moment(day, 'YYYYDDDD')
        }
      )
    );
  }
}
