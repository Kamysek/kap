import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA } from '@angular/material';

@Component({
  selector: 'kap-new-user-dialog',
  templateUrl: './new-user-dialog.component.html',
  styleUrls: ['./new-user-dialog.component.scss']
})
export class NewUserDialogComponent implements OnInit {
  userForm;
  showPasswordHint = false;

  constructor(fb: FormBuilder, @Inject(MAT_DIALOG_DATA) private user: any) {
    this.userForm = fb.group({
      username: ['', Validators.required],
      email: ['', Validators.required],
      timeslotsNeeded: [1],
      emailNotification: [false, Validators.required],
      password: ['', Validators.required],
      group: ['Patient', Validators.required]
    });
  }

  ngOnInit(): void {
    if (this.user) {
      this.userForm.patchValue(this.user);
      this.showPasswordHint = true;
      this.userForm.get('password').setValidators(null);
    }
  }
}
