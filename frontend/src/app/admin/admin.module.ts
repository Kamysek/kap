import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppointmentsComponent } from './appointments/appointments.component';
import { RouterModule, Routes } from '@angular/router';
import { UsersComponent } from './users/users.component';
import { AdminComponent } from './admin.component';
import { UsersResolver } from './resolvers/users.resolver';
import { NewUserDialogComponent } from './users/new-user-dialog/new-user-dialog.component';
import { AuthGuard } from '../guards/auth.guard';
import { AppointmentResolver } from './resolvers/appointment.resolver';
import { SharedModule } from '../shared/shared.module';
import { AddAppointmentsDialogComponent } from './appointments/add-appointments-dialog/add-appointments-dialog.component';
import { StudyPlanComponent } from './study-plan/study-plan.component';
import { PlanResolver } from './resolvers/plan.resolver';
import { DisplayStudyPlanComponent } from './study-plan/display-study-plan/display-study-plan.component';
import { OverduePatientsComponent } from './overdue-patients/overdue-patients.component';
import { EditAppointmentDialogComponent } from './appointments/edit-appointment-dialog/edit-appointment-dialog.component';
import { FailedAppointmentsDialogComponent } from './appointments/failed-appointments-dialog/failed-appointments-dialog.component';

const routes: Routes = [
  {
    path: 'admin',
    component: AdminComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path: 'appointments',
        component: AppointmentsComponent,
        resolve: { appointments: AppointmentResolver }
      },
      {
        path: 'users',
        component: UsersComponent,
        resolve: {
          users: UsersResolver
        }
      },
      {
        path: 'plan',
        component: StudyPlanComponent,
        resolve: {
          plans: PlanResolver
        }
      },
      {
        path: 'overdue',
        component: OverduePatientsComponent
      }
    ]
  }
];

@NgModule({
  declarations: [
    AppointmentsComponent,
    UsersComponent,
    AdminComponent,
    NewUserDialogComponent,
    AddAppointmentsDialogComponent,
    StudyPlanComponent,
    DisplayStudyPlanComponent,
    OverduePatientsComponent,
    EditAppointmentDialogComponent,
    FailedAppointmentsDialogComponent
  ],
  imports: [CommonModule, RouterModule.forChild(routes), SharedModule],
  entryComponents: [
    NewUserDialogComponent,
    AddAppointmentsDialogComponent,
    EditAppointmentDialogComponent,
    FailedAppointmentsDialogComponent
  ]
})
export class AdminModule {}
