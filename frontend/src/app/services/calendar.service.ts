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

  getCalendar(id: any) {
    const variables = { id };
    return this.apollo
      .watchQuery<getCalendar, getCalendarVariables>({
        query: CalendarService.GET_CALENDAR_QUERY,
        variables
      })
      .valueChanges.pipe(map(res => res.data.getCalendar));
  }
}
