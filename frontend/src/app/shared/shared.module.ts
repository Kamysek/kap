import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WeekSwitcherComponent } from './components/week-switcher/week-switcher.component';
import { AppointmentWeekComponent } from './components/appointment-week/appointment-week.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import {
  ErrorStateMatcher,
  ShowOnDirtyErrorStateMatcher
} from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import {
  MAT_DIALOG_DEFAULT_OPTIONS,
  MatDialogModule
} from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatSelectModule } from '@angular/material/select';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import {
  MAT_SNACK_BAR_DEFAULT_OPTIONS,
  MatSnackBarModule
} from '@angular/material/snack-bar';
import { MatTableModule } from '@angular/material/table';
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
