import { Injectable } from '@angular/core';
import gql from 'graphql-tag';
import { Apollo } from 'apollo-angular';
import { getAppointments } from '../../../__generated__/getAppointments';
import { map } from 'rxjs/operators';
import * as moment from 'moment';
import { CreateAppointmentInput } from '../../../__generated__/globalTypes';

@Injectable({
  providedIn: 'root'
})
export class AppointmentsService {
  private static GET_APPOINTMENTS_QUERY = gql`
    query getAppointments {
      getAppointments {
        edges {
          node {
            id
            taken
            appointmentStart
            appointmentEnd
          }
        }
      }
    }
  `;

  private static CREATE_APPOINTMENT_MUTATION = gql`
    mutation createAppointment($appointment: CreateAppointmentInput!) {
      createAppointment(input: $appointment) {
        appointment {
          id
        }
      }
    }
  `;

  constructor(private apollo: Apollo) {}

  public getAppointments() {
    return this.apollo
      .watchQuery<getAppointments>({
        query: AppointmentsService.GET_APPOINTMENTS_QUERY
      })
      .valueChanges.pipe(
        map(appts =>
          appts.data.getAppointments.edges.map(item =>
            Object.assign({}, item.node, {
              startMoment: moment(item.node.appointmentStart),
              endMoment: moment(item.node.appointmentEnd)
            })
          )
        )
      );
  }

  public getWeeks() {
    return this.getAppointments().pipe(
      map(appts => {
        const weeks = {};
        appts.forEach(appt => {
          const week = appt.startMoment.year() * 100 + appt.startMoment.week();
          const day = appt.startMoment.day();
          const morningMoment = moment(appt.startMoment);
          morningMoment.startOf('day');
          morningMoment.add(8, 'hours');
          const startMinute = Math.round(
            appt.startMoment.diff(morningMoment, 'minutes') / 15
          );
          const endMinute = Math.round(
            appt.endMoment.diff(morningMoment, 'minutes') / 15
          );
          if (!weeks[week]) {
            weeks[week] = [];
          }
          weeks[week].push({ ...appt, day, startMinute, endMinute });
        });
        return weeks;
      })
    );
  }

  public createAppointment(input: CreateAppointmentInput) {
    return this.apollo.mutate({
      mutation: AppointmentsService.CREATE_APPOINTMENT_MUTATION,
      variables: { appointment: input }
    });
  }

  public createAppointments(appointments: CreateAppointmentInput[]) {
    return Promise.all(
      appointments.map(appointment =>
        this.createAppointment(appointment).toPromise()
      )
    );
  }
}
