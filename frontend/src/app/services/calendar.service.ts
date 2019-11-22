import { Injectable } from '@angular/core';
import { Apollo } from 'apollo-angular';
import gql from 'graphql-tag';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class CalendarService {
  constructor(private apollo: Apollo) {}

  createNew(calendarInput: { name: string }) {
    const updateQuery = gql`
      query calendars {
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
    const variables = { calendarInput };
    this.apollo
      .mutate({
        mutation: query,
        variables,
        refetchQueries: [{ query: updateQuery }]
      })
      .subscribe(console.log);
  }

  getCalendars() {
    const query = gql`
      query calendars {
        allCalendars {
          name
          id
        }
      }
    `;
    return this.apollo
      .watchQuery<any>({ query })
      .valueChanges.pipe(map(res => res.data.allCalendars));
  }
}
