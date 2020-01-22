import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'kap-collect-comment-dialog',
  templateUrl: './collect-comment-dialog.component.html',
  styleUrls: ['./collect-comment-dialog.component.scss']
})
export class CollectCommentDialogComponent implements OnInit {
  commentControl = new FormControl('', Validators.required);

  constructor(@Inject(MAT_DIALOG_DATA) public slot: any) {}

  ngOnInit() {}
}
