import { first } from 'rxjs/operators';
import { Observable } from 'rxjs';
import {
  ActivatedRouteSnapshot,
  Resolve,
  RouterStateSnapshot
} from '@angular/router';
import { Injectable } from '@angular/core';
import { UserService } from '../../services/user.service';

@Injectable({ providedIn: 'root' })
export class UsersResolver implements Resolve<any> {
  constructor(private usersService: UserService) {}

  resolve(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<any> | Promise<any> | any {
    return this.usersService.getUsers().pipe(first());
  }
}
