import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PatientComponent } from './patient.component';
import { RouterModule, Routes } from '@angular/router';
import { AppointmentOverviewComponent } from './appointment-overview/appointment-overview.component';
import { PatientDataComponent } from './patient-data/patient-data.component';
import { AuthGuard } from '../guards/auth.guard';
import { SurveyOverviewComponent } from './survey-overview/survey-overview.component';
import { SharedModule } from '../shared/shared.module';
import { CollectCommentDialogComponent } from './collect-comment-dialog/collect-comment-dialog.component';

const routes: Routes = [
  { path: 'patient', component: PatientComponent, canActivate: [AuthGuard] }
];

@NgModule({
  declarations: [
    PatientComponent,
    AppointmentOverviewComponent,
    PatientDataComponent,
    SurveyOverviewComponent,
    CollectCommentDialogComponent
  ],
  entryComponents: [CollectCommentDialogComponent],
  imports: [CommonModule, RouterModule.forChild(routes), SharedModule]
})
export class PatientModule {}
