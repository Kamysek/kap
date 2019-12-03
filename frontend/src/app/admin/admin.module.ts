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
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatSelectModule,
  MatTableModule
} from '@angular/material';
import { NewCalendarDialogComponent } from './appointments/new-calendar-dialog/new-calendar-dialog.component';
import { ReactiveFormsModule } from '@angular/forms';
import { EditCalendarComponent } from './appointments/edit-calendar/edit-calendar.component';
import { CalendarResolver } from './resolvers/calendar.resolver';
import { AppointmentListComponent } from './appointments/edit-calendar/appointment-list/appointment-list.component';
import { NewAppointmentComponent } from './appointments/edit-calendar/new-appointment/new-appointment.component';
import { AppointmentFormComponent } from './appointments/edit-calendar/appointment-form/appointment-form.component';
import { MatMomentDateModule } from '@angular/material-moment-adapter';
import { ViewAppointmentComponent } from './appointments/edit-calendar/appointment-list/view-appointment/view-appointment.component';
import { AppointmentResolver } from './resolvers/appointment.resolver';
import { AppointmentInfoComponent } from './appointments/edit-calendar/appointment-list/view-appointment/appointment-info/appointment-info.component';
import { UsersComponent } from './users/users.component';
import { AdminComponent } from './admin.component';
import { UsersResolver } from './resolvers/users.resolver';
import { NewUserDialogComponent } from './users/new-user-dialog/new-user-dialog.component';

const routes: Routes = [
  {
    path: 'admin',
    component: AdminComponent,
    children: [
      {
        path: 'calendars',
        component: AppointmentsComponent,
        children: [
          {
            path: ':id',
            component: EditCalendarComponent,
            resolve: { calendar: CalendarResolver },
            children: [
              {
                path: 'view/:appointmentId',
                component: ViewAppointmentComponent,
                resolve: { appointment: AppointmentResolver }
              }
            ]
          }
        ]
      },
      {
        path: 'users',
        component: UsersComponent,
        resolve: {
          users: UsersResolver
        }
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
    AppointmentFormComponent,
    ViewAppointmentComponent,
    AppointmentInfoComponent,
    UsersComponent,
    AdminComponent,
    NewUserDialogComponent
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
    MatMomentDateModule,
    MatIconModule,
    MatTableModule,
    MatSelectModule
  ],
  entryComponents: [NewCalendarDialogComponent, NewUserDialogComponent]
})
export class AdminModule {}
