import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'kap-new-user-dialog',
  templateUrl: './new-user-dialog.component.html',
  styleUrls: ['./new-user-dialog.component.scss']
})
export class NewUserDialogComponent {
  userForm;

  constructor(fb: FormBuilder) {
    this.userForm = fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
      group: ['', Validators.required]
    });
  }
}
