import { Injectable } from '@angular/core';
import { Apollo } from 'apollo-angular';
import gql from 'graphql-tag';
import { map, switchMap } from 'rxjs/operators';
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
  getAppointmentsForCalendar,
  getAppointmentsForCalendarVariables
} from '../../../__generated__/getAppointmentsForCalendar';

@Injectable({
  providedIn: 'root'
})
export class CalendarService {
  private static ALL_CALENDARS_QUERY = gql`
    query allCalendars {
      getAllCalendars {
        name
        id
      }
    }
  `;

  private static GET_CALENDAR_QUERY = gql`
    query getCalendar($id: Int!) {
      getCalendar(id: $id) {
        id
        name
        doctor {
          username
          id
        }
      }
    }
  `;

  private static GET_APPOINTMENTS_FOR_CALENDAR = gql`
    query getAppointmentsForCalendar($id: Int!) {
      getAllAppointmentsFromCalendar(id: $id) {
        id
        appointmentStart
        appointmentEnd
        title
        taken
      }
    }
  `;

  private static CREATE_CALENDAR_MUTATION = gql`
    mutation createCalendar($calendarInput: CalendarInput!) {
      createCalendar(input: $calendarInput) {
        calendar {
          id
          name
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
      .valueChanges.pipe(map(res => res.data.getAllCalendars));
  }

  getCalendar(id: any) {
    const variables = { id };
    return this.apollo
      .watchQuery<getCalendar, getCalendarVariables>({
        query: CalendarService.GET_CALENDAR_QUERY,
        variables
      })
      .valueChanges.pipe(
        switchMap(calendarRes =>
          this.apollo
            .watchQuery<
              getAppointmentsForCalendar,
              getAppointmentsForCalendarVariables
            >({
              query: CalendarService.GET_APPOINTMENTS_FOR_CALENDAR,
              variables
            })
            .valueChanges.pipe(
              map(appointmentRes =>
                Object.assign({}, calendarRes.data.getCalendar, {
                  appointments:
                    appointmentRes.data.getAllAppointmentsFromCalendar
                })
              )
            )
        )
      );
  }
}
