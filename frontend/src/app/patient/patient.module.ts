import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PatientComponent } from './patient.component';
import { RouterModule, Routes } from '@angular/router';
import { AppointmentOverviewComponent } from './appointment-overview/appointment-overview.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatButtonModule } from '@angular/material';

const routes: Routes = [{ path: 'patient', component: PatientComponent }];

@NgModule({
  declarations: [PatientComponent, AppointmentOverviewComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FlexLayoutModule,
    MatButtonModule
  ]
})
export class PatientModule {}
