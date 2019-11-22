import { Injectable } from '@angular/core';
import { Apollo } from 'apollo-angular';
import gql from 'graphql-tag';
import { map } from 'rxjs/operators';
import {
  createCalendar,
  createCalendarVariables
} from '../../../__generated__/createCalendar';
import { allCalendars } from '../../../__generated__/allCalendars';

@Injectable({
  providedIn: 'root'
})
export class CalendarService {
  constructor(private apollo: Apollo) {}

  createNew(calendarInput: { name: string }) {
    const updateQuery = gql`
      query allCalendars {
        allCalendars {
          name
          id
        }
      }
    `;
    const query = gql`
      mutation createCalendar($calendarInput: CalendarInput!) {
        createCalendar(input: $calendarInput) {
          calendar {
            id
            name
          }
        }
      }
    `;
    const variables: createCalendarVariables = { calendarInput };
    this.apollo
      .mutate<createCalendar>({
        mutation: query,
        variables,
        refetchQueries: [{ query: updateQuery }]
      })
      .subscribe(console.log);
  }

  getCalendars() {
    const query = gql`
      query allCalendars {
        allCalendars {
          name
          id
        }
      }
    `;
    return this.apollo
      .watchQuery<allCalendars>({ query })
      .valueChanges.pipe(map(res => res.data.allCalendars));
  }

  getCalendar(id: any) {
    const query = gql`query getCalendar($id: ID!){
        
    }`;
  }
}
