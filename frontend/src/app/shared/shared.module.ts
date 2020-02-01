import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WeekSwitcherComponent } from './components/week-switcher/week-switcher.component';
import { AppointmentWeekComponent } from './components/appointment-week/appointment-week.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import {
  ErrorStateMatcher,
  MAT_DIALOG_DEFAULT_OPTIONS,
  MAT_SNACK_BAR_DEFAULT_OPTIONS,
  MatButtonModule,
  MatCardModule,
  MatCheckboxModule,
  MatDatepickerModule,
  MatDialogModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatSelectModule,
  MatSlideToggleModule,
  MatSnackBarModule,
  MatTableModule,
  ShowOnDirtyErrorStateMatcher
} from '@angular/material';
import { ReactiveFormsModule } from '@angular/forms';
import { MatMomentDateModule } from '@angular/material-moment-adapter';

const exportedModules = [
  FlexLayoutModule,
  MatButtonModule,
  MatCardModule,
  MatCheckboxModule,
  MatDatepickerModule,
  MatDialogModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatMomentDateModule,
  MatSelectModule,
  MatSlideToggleModule,
  MatSnackBarModule,
  MatTableModule,
  ReactiveFormsModule
];

@NgModule({
  declarations: [WeekSwitcherComponent, AppointmentWeekComponent],
  imports: [CommonModule, exportedModules],
  exports: [WeekSwitcherComponent, exportedModules],
  providers: [
    { provide: MAT_SNACK_BAR_DEFAULT_OPTIONS, useValue: { duration: 3000 } },
    { provide: ErrorStateMatcher, useClass: ShowOnDirtyErrorStateMatcher },
    {
      provide: MAT_DIALOG_DEFAULT_OPTIONS,
      useValue: {
        minWidth: '50vw',
        closeOnNavigation: true,
        disableClose: false,
        hasBackdrop: true
      }
    }
  ]
})
export class SharedModule {}
