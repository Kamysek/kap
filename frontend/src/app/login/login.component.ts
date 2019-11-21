import {ChangeDetectionStrategy, Component} from '@angular/core';
import {FormBuilder, Validators} from '@angular/forms';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'kap-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LoginComponent {

  loginForm;

  constructor(fb: FormBuilder, private http: HttpClient) {
    this.loginForm = fb.group({username: ['', Validators.required], password: ['', Validators.required]});
  }

  submitForm() {
    const query = `mutation{tokenAuth(username:"${this.loginForm.value.username}", password:"${this.loginForm.value.password}"){token}}`;
    this.http.post('/graphql/', {query}).subscribe(console.log);
  }
}
