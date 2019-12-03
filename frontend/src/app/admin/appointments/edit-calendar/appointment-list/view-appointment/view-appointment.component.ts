import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { map } from 'rxjs/operators';

@Component({
  selector: 'kap-view-appointment',
  templateUrl: './view-appointment.component.html',
  styleUrls: ['./view-appointment.component.scss']
})
export class ViewAppointmentComponent implements OnInit {
  appointment$;

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.appointment$ = this.route.data.pipe(map(data => data.appointment));
  }
}
