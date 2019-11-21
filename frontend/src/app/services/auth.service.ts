import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private authToken: string;

  constructor(private http: HttpClient) {
    this.authToken = localStorage.getItem('kap-token');
  }

  get authorization() {
    return this.authenticated ? {Authorization: `JWT ${this.authToken}`} : {};
  }

  get authenticated() {
    return !!this.authToken;
  }

  login(username: string, password: string) {
    const query = `mutation($username: String!, $password: String!){tokenAuth(username:$username, password:$password){token}}`;
    const variables = {username, password};
    this.http.post<{ data?: { tokenAuth: { token: string } } }>('/graphql/', {query, variables}).subscribe(res => {
      console.log(res);
      if (res.hasOwnProperty('data')) {
        this.authToken = res.data.tokenAuth.token;
        localStorage.setItem('kap-token', this.authToken);
      }
    });
  }

  logout() {
    this.authToken = null;
    localStorage.setItem('kap-token', this.authToken);
  }
}
