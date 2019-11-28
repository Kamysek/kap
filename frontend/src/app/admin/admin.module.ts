import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppointmentsComponent } from './appointments/appointments.component';
import { RouterModule, Routes } from '@angular/router';
import { FlexLayoutModule } from '@angular/flex-layout';
import {
  MatButtonModule,
  MatDatepickerModule,
  MatDialogModule,
  MatFormFieldModule,
  MatInputModule,
  MatListModule
} from '@angular/material';
import { NewCalendarDialogComponent } from './appointments/new-calendar-dialog/new-calendar-dialog.component';
import { ReactiveFormsModule } from '@angular/forms';
import { EditCalendarComponent } from './appointments/edit-calendar/edit-calendar.component';
import { CalendarResolver } from './resolvers/calendar.resolver';
import { AppointmentListComponent } from './appointments/edit-calendar/appointment-list/appointment-list.component';
import { NewAppointmentComponent } from './appointments/edit-calendar/new-appointment/new-appointment.component';
import { AppointmentFormComponent } from './appointments/edit-calendar/appointment-form/appointment-form.component';
import { MatMomentDateModule } from '@angular/material-moment-adapter';

const routes: Routes = [
  {
    path: 'admin',
    children: [
      {
        path: 'appointments',
        component: AppointmentsComponent,
        children: [
          {
            path: ':id',
            component: EditCalendarComponent,
            resolve: { calendar: CalendarResolver }
          }
        ]
      }
    ]
  }
];

@NgModule({
  declarations: [
    AppointmentsComponent,
    NewCalendarDialogComponent,
    EditCalendarComponent,
    AppointmentListComponent,
    NewAppointmentComponent,
    AppointmentFormComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FlexLayoutModule,
    MatListModule,
    MatButtonModule,
    MatDialogModule,
    ReactiveFormsModule,
    MatInputModule,
    MatFormFieldModule,
    MatDatepickerModule,
    MatMomentDateModule
  ],
  entryComponents: [NewCalendarDialogComponent]
})
export class AdminModule {}
