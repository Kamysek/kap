import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppointmentsComponent } from './appointments/appointments.component';
import { RouterModule, Routes } from '@angular/router';
import { FlexLayoutModule } from '@angular/flex-layout';
import {
  MatButtonModule,
  MatDialogModule,
  MatInputModule,
  MatListModule
} from '@angular/material';
import { NewCalendarDialogComponent } from './appointments/new-calendar-dialog/new-calendar-dialog.component';
import { ReactiveFormsModule } from '@angular/forms';

const routes: Routes = [
  {
    path: 'admin',
    children: [{ path: 'appointments', component: AppointmentsComponent }]
  }
];

@NgModule({
  declarations: [AppointmentsComponent, NewCalendarDialogComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FlexLayoutModule,
    MatListModule,
    MatButtonModule,
    MatDialogModule,
    ReactiveFormsModule,
    MatInputModule
  ],
  entryComponents: [NewCalendarDialogComponent]
})
export class AdminModule {}
