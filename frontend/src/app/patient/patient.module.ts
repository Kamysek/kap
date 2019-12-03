import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PatientComponent } from './patient.component';
import { RouterModule, Routes } from '@angular/router';
import { AppointmentOverviewComponent } from './appointment-overview/appointment-overview.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatButtonModule } from '@angular/material';
import { PatientDataComponent } from './patient-data/patient-data.component';
import { AuthGuard } from '../guards/auth.guard';
import { SurveyOverviewComponent } from './survey-overview/survey-overview.component';

const routes: Routes = [
  { path: 'patient', component: PatientComponent, canActivate: [AuthGuard] }
];

@NgModule({
  declarations: [
    PatientComponent,
    AppointmentOverviewComponent,
    PatientDataComponent,
    SurveyOverviewComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FlexLayoutModule,
    MatButtonModule
  ]
})
export class PatientModule {}
