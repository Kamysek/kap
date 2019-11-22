import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'kap-new-calendar-dialog',
  templateUrl: './new-calendar-dialog.component.html',
  styleUrls: ['./new-calendar-dialog.component.scss']
})
export class NewCalendarDialogComponent implements OnInit {
  calendarForm;

  constructor(fb: FormBuilder) {
    this.calendarForm = fb.group({
      name: ['', Validators.required]
    });
  }

  ngOnInit() {}
}
