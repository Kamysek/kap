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
    this.authToken = localStorage.getItem('kap-token');
    this.group = localStorage.getItem('kap-group');
  }

  get authorization() {
    return this.authenticated ? { Authorization: `JWT ${this.authToken}` } : {};
  }

  get authenticated() {
    return !!this.authToken;
  }

  login(username: string, password: string) {
    const query = `mutation($username: String!, $password: String!){tokenAuth(username:$username, password:$password){token}}`;
    const variables = { username, password };
    this.http
      .post<{ data?: { tokenAuth: { token: string } } }>('/graphql/', {
        query,
        variables
      })
      .subscribe(res => {
        console.log(res);
        if (res.hasOwnProperty('data')) {
          this.authToken = res.data.tokenAuth.token;
          localStorage.setItem('kap-token', this.authToken);
          this.http
            .post<{ data?: { getUserGroup: string } }>('/graphql/', {
              query: `query{getUserGroup}`
            })
            .subscribe(groupRes => {
              if (groupRes.hasOwnProperty('data')) {
                this.group = groupRes.data.getUserGroup;
                localStorage.setItem('kap-group', this.group);
                switch (this.group) {
                  case 'Admin': {
                    this.router.navigate(['/admin/appointments']);
                    break;
                  }
                  default: {
                    this.router.navigate(['/patient']);
                    break;
                  }
                }
              }
            });
        }
      });
  }

  logout() {
    this.authToken = null;
    localStorage.removeItem('kap-token');
    this.group = null;
    localStorage.removeItem('kap-group');
    this.router.navigate(['login']);
  }
}
