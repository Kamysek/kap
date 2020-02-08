import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private authToken: string;
  private group: string;

  constructor(private http: HttpClient, private router: Router) {
    this.authToken = sessionStorage.getItem('kap-token');
    this.group = sessionStorage.getItem('kap-group');
  }

  get authorization() {
    return this.authenticated ? { Authorization: `JWT ${this.authToken}` } : {};
  }

  get authenticated() {
    return !!this.authToken;
  }

  async login(username: string, password: string) {
    const query = `mutation($username: String!, $password: String!){tokenAuth(username:$username, password:$password){token}}`;
    const variables = { username, password };
    const res = await this.http
      .post<{ data?: { tokenAuth: { token: string } } }>('/graphql/', {
        query,
        variables
      })
      .toPromise();
    if (!!res.data.tokenAuth) {
      this.authToken = res.data.tokenAuth.token;
      sessionStorage.setItem('kap-token', this.authToken);
      const groupRes = await this.http
        .post<{ data?: { getUserGroup: string } }>('/graphql/', {
          query: `query{getUserGroup}`
        })
        .toPromise();
      if (groupRes.hasOwnProperty('data')) {
        this.group = groupRes.data.getUserGroup;
        sessionStorage.setItem('kap-group', this.group);
        switch (this.group) {
          case 'Admin': {
            await this.router.navigate(['/admin/appointments']);
            break;
          }
          case 'Doctor': {
            await this.router.navigate(['/doctor']);
            break;
          }
          case 'Labor': {
            await this.router.navigate(['/lab']);
            break;
          }
          default: {
            await this.router.navigate(['/patient']);
            break;
          }
        }
        return true;
      }
    } else {
      return false;
    }
  }

  logout() {
    this.authToken = null;
    sessionStorage.removeItem('kap-token');
    this.group = null;
    sessionStorage.removeItem('kap-group');
    this.router.navigate(['login']);
  }
}
