import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

@Component({
  selector: 'kap-patient-data',
  templateUrl: './patient-data.component.html',
  styleUrls: ['./patient-data.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PatientDataComponent {
  @Input() patient;
}
