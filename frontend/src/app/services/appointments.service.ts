import { Injectable } from '@angular/core';
import gql from 'graphql-tag';
import { Apollo } from 'apollo-angular';
import { getAppointments } from '../../../__generated__/getAppointments';
import { map } from 'rxjs/operators';
import * as moment from 'moment';
import 'moment-timezone';
import {
  AppointmentInput,
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
  getWeekAppointments,
  getWeekAppointmentsVariables
} from '../../../__generated__/getWeekAppointments';
import { UserService } from './user.service';
import {
  getOpenSlots,
  getOpenSlotsVariables
} from '../../../__generated__/getOpenSlots';
import { takeSlot, takeSlotVariables } from '../../../__generated__/takeSlot';
import {
  createAppointments,
  createAppointmentsVariables
} from '../../../__generated__/createAppointments';

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
            patient {
              username
            }
          }
        }
      }
    }
  `;

  private static GET_POSSIBLE_SLOTS = gql`
    query getOpenSlots($minus: Int!, $plus: Int!, $user: ID) {
      getSlotLists(minusdays: $minus, plusdays: $plus, userId: $user) {
        appointmentStart
        appointmentEnd
        id
      }
    }
  `;

  private static GET_WEEK_APPOINTMENTS = gql`
    query getWeekAppointments($after: DateTime!, $before: DateTime!) {
      getAppointments(
        taken: true
        hasPatient: true
        after: $after
        before: $before
      ) {
        edges {
          node {
            id
            title
            taken
            appointmentStart
            appointmentEnd
            commentDoctor
            commentPatient
            noshow
            patient {
              id
              username
              email
            }
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
          patient {
            username
            email
          }
        }
      }
    }
  `;

  private static CREATE_APPOINTMENTS_MUTATION = gql`
    mutation createAppointments($input: CreateAppointmentsInput!) {
      createAppointments(input: $input) {
        appointments {
          appointmentStart
          appointmentEnd
          id
        }
      }
    }
  `;

  private static UPDATE_APPOINTMENT_MUTATION = gql`
    mutation updateAppointment($appointment: UpdateAppointmentInput!) {
      updateAppointment(input: $appointment) {
        appointment {
          id
          taken
          title
          commentPatient
          appointmentStart
          appointmentEnd
        }
      }
    }
  `;

  private static TAKE_SLOT_MUTATION = gql`
    mutation takeSlot($input: BookSlotsInput!) {
      bookSlots(input: $input) {
        appointmentList
      }
    }
  `;

  constructor(private apollo: Apollo, private userService: UserService) {}

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
        // tap(a => console.log(JSON.stringify(a[240])))
      );
  }

  public getFreeSlots(minus = 7, plus = 7, user = null) {
    return this.apollo
      .watchQuery<getOpenSlots, getOpenSlotsVariables>({
        query: AppointmentsService.GET_POSSIBLE_SLOTS,
        variables: {
          minus,
          plus,
          user
        }
      })
      .valueChanges.pipe(
        map(appts =>
          appts.data.getSlotLists.map(slot => {
            const momentAppointments = slot.map(appointment =>
              Object.assign({}, appointment, {
                startMoment: moment(appointment.appointmentStart),
                endMoment: moment(appointment.appointmentEnd)
              })
            );
            momentAppointments.sort(appt => appt.startMoment.valueOf());
            return {
              start: moment(momentAppointments[0].startMoment),
              end: moment(
                momentAppointments[momentAppointments.length - 1].endMoment
              ),
              appointments: momentAppointments.map(appt => appt.id)
            };
          })
        )
      );
  }

  public getCurrentWeekTakenAppointments() {
    return this.apollo
      .watchQuery<getWeekAppointments, getWeekAppointmentsVariables>({
        query: AppointmentsService.GET_WEEK_APPOINTMENTS,
        variables: {
          after: moment()
            .startOf('isoWeek')
            .toDate(),
          before: moment()
            .endOf('isoWeek')
            .add(1, 'week')
            .toDate()
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

  public getDays({ minus, plus, userId = null }) {
    return this.getFreeSlots(minus, plus, userId).pipe(
      map(slots => {
        const days = {};
        slots.forEach(slot => {
          const day = slot.start.year() * 1000 + slot.start.dayOfYear();
          if (!days[day]) {
            days[day] = [];
          }
          days[day].push({ ...slot, day });
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
          morningMoment.hour(0).minute(0);
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

  public createAppointments(appointments: AppointmentInput[]) {
    return this.apollo
      .mutate<createAppointments, createAppointmentsVariables>({
        mutation: AppointmentsService.CREATE_APPOINTMENTS_MUTATION,
        variables: { input: { appointments } },
        refetchQueries: [{ query: AppointmentsService.GET_APPOINTMENTS_QUERY }]
      })
      .pipe(map(res => res.data.createAppointments.appointments));
    /*return Promise.all(
      appointments.map(appointment =>
        this.createAppointment(appointment).toPromise()
      )
    );*/
  }

  public bookSlot(variables: takeSlotVariables, config: getOpenSlotsVariables) {
    return this.apollo.mutate<takeSlot, takeSlotVariables>({
      mutation: AppointmentsService.TAKE_SLOT_MUTATION,
      variables,
      refetchQueries: [
        { query: AppointmentsService.GET_POSSIBLE_SLOTS, variables: config },
        { query: UserService.LOAD_USER_DETAILS }
      ]
    });
  }

  public reportNoShow(id: string) {
    return this.updateAppointment({ id, noshow: true });
  }
}
