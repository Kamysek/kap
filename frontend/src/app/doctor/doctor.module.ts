import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../guards/auth.guard';
import { SharedModule } from '../shared/shared.module';
import { ExamPortalComponent } from './exam-portal/exam-portal.component';

const routes: Routes = [
  { path: 'doctor', component: ExamPortalComponent, canActivate: [AuthGuard] }
];

@NgModule({
  declarations: [ExamPortalComponent],
  imports: [CommonModule, RouterModule.forChild(routes), SharedModule]
})
export class DoctorModule {}
