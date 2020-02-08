import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { first, startWith } from 'rxjs/operators';
import { MatDialog } from '@angular/material/dialog';
import { MatTableDataSource } from '@angular/material/table';
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
    'group',
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
      .open(NewUserDialogComponent, { data: false })
      .afterClosed()
      .subscribe(res => {
        if (!!res) {
          this.usersService.createUser(res);
        }
      });
  }

  editUser(user) {
    this.dialog
      .open(NewUserDialogComponent, { data: user })
      .afterClosed()
      .subscribe(res => {
        if (!!res) {
          if (!res.password) {
            delete res.password;
          }
          this.usersService.updateUser({ id: user.id, ...res });
        }
      });
  }

  ngOnDestroy(): void {
    this.destroyed$.complete();
  }
}
