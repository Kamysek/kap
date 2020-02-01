import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { first, startWith } from 'rxjs/operators';
import { MatDialog, MatTableDataSource } from '@angular/material';
import { FormControl } from '@angular/forms';
import { Subject } from 'rxjs';
import { NewUserDialogComponent } from './new-user-dialog/new-user-dialog.component';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'kap-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit, OnDestroy {
  users$;
  dataSource;
  filterControl = new FormControl();
  displayedColumns: string[] = [
    'email',
    'username',
    'slots',
    'checkup',
    'actions'
  ];
  private destroyed$ = new Subject();

  // @ViewChild(MatSort, { static: true }) sort: MatSort;

  constructor(
    private route: ActivatedRoute,
    private dialog: MatDialog,
    private usersService: UserService
  ) {}

  async ngOnInit() {
    this.users$ = this.usersService
      .getUsers()
      .pipe(startWith(this.route.snapshot.data.users));
    this.dataSource = new MatTableDataSource(
      await this.users$.pipe(first()).toPromise()
    );
    // this.dataSource.sort = this.sort;
    /*this.filterControl.valueChanges
      .pipe(takeUntil(this.destroyed$))
      .subscribe(
        value => (this.dataSource.filter = value.trim().toLowerCase())
      );*/
  }

  createUser() {
    this.dialog
      .open(NewUserDialogComponent)
      .afterClosed()
      .subscribe(res => {
        if (!!res) {
          this.usersService.createUser(res);
        }
      });
  }

  ngOnDestroy(): void {
    this.destroyed$.complete();
  }
}
