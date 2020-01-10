import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WeekSwitcherComponent } from './components/week-switcher/week-switcher.component';
import { AppointmentWeekComponent } from './components/appointment-week/appointment-week.component';
import { FlexLayoutModule } from '@angular/flex-layout';

@NgModule({
  declarations: [WeekSwitcherComponent, AppointmentWeekComponent],
  imports: [CommonModule, FlexLayoutModule],
  exports: [WeekSwitcherComponent]
})
export class SharedModule {}
