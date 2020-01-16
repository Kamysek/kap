import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../shared/shared.module';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../guards/auth.guard';
import { LabOverviewComponent } from './lab-overview/lab-overview.component';
import { AppointmentOverviewComponent } from './lab-overview/appointment-overview/appointment-overview.component';

const routes: Routes = [
  { path: 'lab', component: LabOverviewComponent, canActivate: [AuthGuard] }
];

@NgModule({
  declarations: [LabOverviewComponent, AppointmentOverviewComponent],
  imports: [CommonModule, RouterModule.forChild(routes), SharedModule]
})
export class LabModule {}
