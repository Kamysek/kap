import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'kap-overdue-patients',
  templateUrl: './overdue-patients.component.html',
  styleUrls: ['./overdue-patients.component.scss']
})
export class OverduePatientsComponent implements OnInit {
  patients;
  commentControl = new FormControl('', Validators.required);

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.patients = this.userService.getOverdueUsers();
  }

  async recordCall(user) {
    await this.userService
      .recordCall({
        recordInput: { comment: this.commentControl.value, userId: user.id }
      })
      .toPromise();
    this.commentControl.reset('');
  }
}
