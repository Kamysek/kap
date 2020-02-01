import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../guards/auth.guard';
import { SharedModule } from '../shared/shared.module';
import { ExamPortalComponent } from './exam-portal/exam-portal.component';
import { MakeAppointmentDialogComponent } from './exam-portal/make-appointment-dialog/make-appointment-dialog.component';

const routes: Routes = [
  { path: 'doctor', component: ExamPortalComponent, canActivate: [AuthGuard] }
];

@NgModule({
  declarations: [ExamPortalComponent, MakeAppointmentDialogComponent],
  entryComponents: [MakeAppointmentDialogComponent],
  imports: [CommonModule, RouterModule.forChild(routes), SharedModule]
})
export class DoctorModule {}
