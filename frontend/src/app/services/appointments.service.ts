import { Injectable } from '@angular/core';
import gql from 'graphql-tag';
import { Apollo } from 'apollo-angular';
import { getAppointments } from '../../../__generated__/getAppointments';
import { map } from 'rxjs/operators';
import * as moment from 'moment';
import {
  CreateAppointmentInput,
  UpdateAppointmentInput
} from '../../../__generated__/globalTypes';
import {
  updateAppointment,
  updateAppointmentVariables
} from '../../../__generated__/updateAppointment';
import {
  createAppointment,
  createAppointmentVariables
} from '../../../__generated__/createAppointment';
import {
  getFreeAppointments,
  getFreeAppointmentsVariables
} from '../../../__generated__/getFreeAppointments';
import {
  getWeekAppointments,
  getWeekAppointmentsVariables
} from '../../../__generated__/getWeekAppointments';

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
            title
            taken
            appointmentStart
            appointmentEnd
            commentDoctor
            commentPatient
          }
        }
      }
    }
  `;

  private static GET_FREE_APPOINTMENTS = gql`
    query getFreeAppointments($after: String!) {
      getAppointments(taken: false, after: $after) {
        edges {
          node {
            id
            title
            taken
            appointmentStart
            appointmentEnd
            commentDoctor
            commentPatient
          }
        }
      }
    }
  `;

  private static GET_WEEK_APPOINTMENTS = gql`
    query getWeekAppointments($after: String!, $before: String!) {
      getAppointments(taken: true, after: $after, before: $before) {
        edges {
          node {
            id
            title
            taken
            appointmentStart
            appointmentEnd
            commentDoctor
            commentPatient
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
          title
          taken
          appointmentStart
          appointmentEnd
          commentDoctor
          commentPatient
        }
      }
    }
  `;

  private static UPDATE_APPOINTMENT_MUTATION = gql`
    mutation updateAppointment($appointment: UpdateAppointmentInput!) {
      updateAppointment(input: $appointment) {
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

  public getFreeAppointments() {
    return this.apollo
      .watchQuery<getFreeAppointments, getFreeAppointmentsVariables>({
        query: AppointmentsService.GET_FREE_APPOINTMENTS,
        variables: {
          after: moment()
            .toDate()
            .toString()
        }
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

  public getCurrentWeekTakenAppointments() {
    return this.apollo
      .watchQuery<getWeekAppointments, getWeekAppointmentsVariables>({
        query: AppointmentsService.GET_WEEK_APPOINTMENTS,
        variables: {
          after: moment()
            .startOf('week')
            .toDate()
            .toString(),
          before: moment()
            .endOf('week')
            .toDate()
            .toString()
        }
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

  public getDays() {
    return this.getFreeAppointments().pipe(
      map(appts => {
        const days = {};
        appts.forEach(appt => {
          const day =
            appt.startMoment.year() * 1000 + appt.startMoment.dayOfYear();
          if (!days[day]) {
            days[day] = [];
          }
          days[day].push({ ...appt, day });
        });
        return days;
      })
    );
  }

  public getCurrentWeek() {
    return this.getCurrentWeekTakenAppointments().pipe(
      map(appts => {
        const days = {};
        appts.forEach(appt => {
          const day =
            appt.startMoment.year() * 1000 + appt.startMoment.dayOfYear();
          if (!days[day]) {
            days[day] = [];
          }
          days[day].push({ ...appt, day });
        });
        return days;
      })
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
    return this.apollo.mutate<createAppointment, createAppointmentVariables>({
      mutation: AppointmentsService.CREATE_APPOINTMENT_MUTATION,
      variables: { appointment: input },
      update: (
        store,
        {
          data: {
            createAppointment: { appointment }
          }
        }
      ) => {
        const data = store.readQuery<getAppointments>({
          query: AppointmentsService.GET_APPOINTMENTS_QUERY
        });
        data.getAppointments.edges = [
          ...data.getAppointments.edges,
          { node: appointment, __typename: 'AppointmentTypeEdge' }
        ];
        store.writeQuery({
          query: AppointmentsService.GET_APPOINTMENTS_QUERY,
          data
        });
      }
    });
  }

  public updateAppointment(input: UpdateAppointmentInput) {
    return this.apollo.mutate<updateAppointment, updateAppointmentVariables>({
      mutation: AppointmentsService.UPDATE_APPOINTMENT_MUTATION,
      variables: { appointment: input },
      refetchQueries: [{ query: AppointmentsService.GET_APPOINTMENTS_QUERY }]
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
