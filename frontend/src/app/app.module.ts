import { BrowserModule } from '@angular/platform-browser';
import { LOCALE_ID, NgModule } from '@angular/core';
import localeEn from '@angular/common/locales/en-DE';
import localeEnExtra from '@angular/common/locales/extra/en-DE';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LoginComponent } from './login/login.component';
import {
  HTTP_INTERCEPTORS,
  HttpClientModule,
  HttpClientXsrfModule
} from '@angular/common/http';
import { AuthInterceptor } from './services/auth.interceptor';
import { AdminModule } from './admin/admin.module';
import { GraphQLModule } from './graphql.module';
import { MAT_DATE_LOCALE } from '@angular/material/core';
import { registerLocaleData } from '@angular/common';
import { PatientModule } from './patient/patient.module';
import { SharedModule } from './shared/shared.module';
import { LabModule } from './lab/lab.module';
import { DoctorModule } from './doctor/doctor.module';
import { MAT_FORM_FIELD_DEFAULT_OPTIONS } from '@angular/material/form-field';

registerLocaleData(localeEn, 'en-DE', localeEnExtra);

@NgModule({
  declarations: [AppComponent, LoginComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken'
    }),
    BrowserAnimationsModule,
    SharedModule,
    AdminModule,
    PatientModule,
    DoctorModule,
    LabModule,
    GraphQLModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    { provide: MAT_DATE_LOCALE, useValue: 'de-DE' },
    {
      provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,
      useValue: { appearance: 'fill' }
    },
    { provide: LOCALE_ID, useValue: 'en-DE' }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
