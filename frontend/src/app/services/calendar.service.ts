import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CalendarService {

  constructor(private http: HttpClient) {
  }

    createNew(calendarInput: { name: string }) {
        const query = `mutation createCalendar($calendarInput: CalendarInput!){
            createCalendar(input: $calendarInput){
                calendar{
                    id
                }
            }
        }`;
        const variables = {calendarInput};
        this.http.post('/graphql/', {query, variables}).subscribe(console.log);
    }
}
