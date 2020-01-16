import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppointmentsComponent } from './appointments/appointments.component';
import { RouterModule, Routes } from '@angular/router';
import { FlexLayoutModule } from '@angular/flex-layout';
import {
  MatButtonModule,
  MatCheckboxModule,
  MatDatepickerModule,
  MatDialogModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatSelectModule,
  MatTableModule
} from '@angular/material';
import { ReactiveFormsModule } from '@angular/forms';
import { MatMomentDateModule } from '@angular/material-moment-adapter';
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
        /*resolve: {
          plans: PlanResolver
        }*/
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
    OverduePatientsComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FlexLayoutModule,
    SharedModule,
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
    MatSelectModule,
    MatCheckboxModule
  ],
  entryComponents: [NewUserDialogComponent, AddAppointmentsDialogComponent]
})
export class AdminModule {}
