import { Injectable } from '@angular/core';
import { Apollo } from 'apollo-angular';
import gql from 'graphql-tag';
import { map } from 'rxjs/operators';
import {
  createCalendar,
  createCalendarVariables
} from '../../../__generated__/createCalendar';
import { allCalendars } from '../../../__generated__/allCalendars';
import {
  getCalendar,
  getCalendarVariables
} from '../../../__generated__/getCalendar';
import {
  CreateAppointmentInput,
  TakeAppointmentInput
} from '../../../__generated__/globalTypes';
import {
  createAppointment,
  createAppointmentVariables
} from '../../../__generated__/createAppointment';
import {
  getAppointment,
  getAppointmentVariables
} from '../../../__generated__/getAppointment';
import { allAppointments } from '../../../__generated__/allAppointments';
import {
  takeAppointment,
  takeAppointmentVariables
} from '../../../__generated__/takeAppointment';

@Injectable({
  providedIn: 'root'
})
export class CalendarService {
  private static ALL_CALENDARS_QUERY = gql`
    query allCalendars {
      getCalendars {
        edges {
          node {
            name
            id
          }
        }
      }
    }
  `;

  private static CALENDARS_WITH_APPOINTMENTS = gql`
    query allAppointments {
      getCalendars {
        edges {
          node {
            name
            id
            doctor {
              username
            }
            appointmentSet {
              edges {
                node {
                  id
                  title
                  appointmentStart
                  appointmentEnd
                  taken
                  patient {
                    id
                  }
                }
              }
            }
          }
        }
      }
    }
  `;

  private static GET_CALENDAR_QUERY = gql`
    query getCalendar($id: ID!) {
      getCalendar(id: $id) {
        id
        name
        doctor {
          username
          id
        }
        appointmentSet {
          edges {
            node {
              id
              appointmentStart
              appointmentEnd
              title
              taken
            }
          }
        }
      }
    }
  `;

  private static GET_APPOINTMENT_QUERY = gql`
    query getAppointment($id: ID!) {
      getAppointment(id: $id) {
        id
        appointmentStart
        appointmentEnd
        commentDoctor
        commentPatient
        title
        taken
        patient {
          username
        }
      }
    }
  `;

  private static CREATE_CALENDAR_MUTATION = gql`
    mutation createCalendar($calendarInput: CreateCalendarInput!) {
      createCalendar(input: $calendarInput) {
        calendar {
          id
          name
        }
      }
    }
  `;

  private static TAKE_APPOINTMENT_MUTATION = gql`
    mutation takeAppointment($appointmentInput: TakeAppointmentInput!) {
      takeAppointment(input: $appointmentInput) {
        appointment {
          taken
        }
      }
    }
  `;

  private static CREATE_APPOINTMENT_MUTATION = gql`
    mutation createAppointment($appointmentInput: CreateAppointmentInput!) {
      createAppointment(input: $appointmentInput) {
        appointment {
          id
        }
      }
    }
  `;

  constructor(private apollo: Apollo) {}

  createNew(calendarInput: { name: string }) {
    const variables: createCalendarVariables = { calendarInput };
    this.apollo
      .mutate<createCalendar>({
        mutation: CalendarService.CREATE_CALENDAR_MUTATION,
        variables,
        refetchQueries: [{ query: CalendarService.ALL_CALENDARS_QUERY }]
      })
      .subscribe(console.log);
  }

  getCalendars() {
    return this.apollo
      .watchQuery<allCalendars>({ query: CalendarService.ALL_CALENDARS_QUERY })
      .valueChanges.pipe(
        map(res => res.data.getCalendars.edges.map(edge => edge.node))
      );
  }

  getAppointments() {
    return this.apollo
      .watchQuery<allAppointments>({
        query: CalendarService.CALENDARS_WITH_APPOINTMENTS
      })
      .valueChanges.pipe(
        map(res =>
          res.data.getCalendars.edges.map(calEdge =>
            Object.assign({}, calEdge.node, {
              appointments: calEdge.node.appointmentSet.edges.map(
                appEdge => appEdge.node
              )
            })
          )
        )
      );
  }

  getCalendar(id: getCalendarVariables['id']) {
    const variables = { id };
    return this.apollo
      .watchQuery<getCalendar, getCalendarVariables>({
        query: CalendarService.GET_CALENDAR_QUERY,
        variables
      })
      .valueChanges.pipe(
        map(res => res.data.getCalendar),
        map(calendar =>
          Object.assign({}, calendar, {
            appointments: calendar.appointmentSet.edges.map(edge => edge.node)
          })
        )
      );
  }

  getAppointment(id: getAppointmentVariables['id']) {
    const variables = { id };
    return this.apollo
      .watchQuery<getAppointment, getAppointmentVariables>({
        query: CalendarService.GET_APPOINTMENT_QUERY,
        variables
      })
      .valueChanges.pipe(
        map(res => res.data.getAppointment)
        /*map(calendar =>
          Object.assign({}, calendar, {
            appointments: calendar.appointmentSet.edges.map(edge => edge.node)
          })
        )*/
      );
  }

  addAppointment(appointmentInput: CreateAppointmentInput) {
    const variables = { appointmentInput };
    this.apollo
      .mutate<createAppointment, createAppointmentVariables>({
        mutation: CalendarService.CREATE_APPOINTMENT_MUTATION,
        variables,
        refetchQueries: [
          {
            query: CalendarService.GET_CALENDAR_QUERY,
            variables: { id: variables.appointmentInput.calendar }
          }
        ]
      })
      .subscribe(console.log);
  }

  takeAppointment(appointmentInput: TakeAppointmentInput) {
    const variables = { appointmentInput };
    this.apollo
      .mutate<takeAppointment, takeAppointmentVariables>({
        mutation: CalendarService.TAKE_APPOINTMENT_MUTATION,
        variables,
        refetchQueries: [
          {
            query: CalendarService.CALENDARS_WITH_APPOINTMENTS
          }
        ]
      })
      .subscribe(console.log);
  }
}
