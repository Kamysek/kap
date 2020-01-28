import { Injectable } from '@angular/core';
import { Apollo } from 'apollo-angular';
import gql from 'graphql-tag';
import { map } from 'rxjs/operators';
import { getUsers } from '../../../__generated__/getUsers';
import {
  createUser,
  createUserVariables
} from '../../../__generated__/createUser';
import { CreateUserInput } from '../../../__generated__/globalTypes';
import { getUserDetails } from '../../../__generated__/getUserDetails';
import { getOverdue } from '../../../__generated__/getOverdue';
import {
  recordCall,
  recordCallVariables
} from '../../../__generated__/recordCall';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private static LOAD_USERS_QUERY = gql`
    query getUsers {
      getUsers {
        edges {
          node {
            username
            email
            id
            dateJoined
            checkupOverdue
            timeslotsNeeded
          }
        }
      }
    }
  `;

  private static LOAD_OVERDUE_QUERY = gql`
    query getOverdue {
      getOverduePatients {
        edges {
          node {
            username
            email
            id
            dateJoined
            checkupOverdue
            timeslotsNeeded
            callSet {
              edges {
                node {
                  date
                  comment
                  id
                }
              }
            }
          }
        }
      }
    }
  `;

  public static LOAD_USER_DETAILS = gql`
    query getUserDetails {
      getMe {
        id
        username
        email
        dateJoined
        checkupOverdue
      }
    }
  `;

  private static CREATE_USER_MUTATION = gql`
    mutation createUser($userInput: CreateUserInput!) {
      createUser(input: $userInput) {
        user {
          id
        }
      }
    }
  `;

  private static RECORD_CALL_MUTATION = gql`
    mutation recordCall($recordInput: UserCalledInput!) {
      userCalled(input: $recordInput) {
        user {
          callSet {
            edges {
              node {
                comment
                date
                id
              }
            }
          }
        }
      }
    }
  `;

  constructor(private apollo: Apollo) {}

  getUsers() {
    return this.apollo
      .watchQuery<getUsers>({ query: UserService.LOAD_USERS_QUERY })
      .valueChanges.pipe(
        map(res => res.data.getUsers.edges.map(edge => edge.node))
      );
  }

  getOverdueUsers() {
    return this.apollo
      .watchQuery<getOverdue>({ query: UserService.LOAD_OVERDUE_QUERY })
      .valueChanges.pipe(
        map(res =>
          res.data.getOverduePatients.edges.map(edge =>
            Object.assign({}, edge.node, {
              calls: edge.node.callSet.edges.map(callEdge => callEdge.node)
            })
          )
        )
      );
  }

  getOwnDetails() {
    return this.apollo
      .watchQuery<getUserDetails>({ query: UserService.LOAD_USER_DETAILS })
      .valueChanges.pipe(
        map(res => res.data.getMe)
        /*map(me =>
          Object.assign({}, me, {
            appointments: me.appointmentSet.edges.map(edge => edge.node)
          })
        )*/
      );
  }

  createUser(userInput: CreateUserInput) {
    this.apollo
      .mutate<createUser, createUserVariables>({
        mutation: UserService.CREATE_USER_MUTATION,
        variables: {
          userInput: { ...userInput, isActive: true, isStaff: false }
        },
        refetchQueries: [{ query: UserService.LOAD_USERS_QUERY }]
      })
      .subscribe(console.log);
  }

  recordCall(variables: recordCallVariables) {
    return this.apollo.mutate<recordCall, recordCallVariables>({
      mutation: UserService.RECORD_CALL_MUTATION,
      variables,
      refetchQueries: [{ query: UserService.LOAD_OVERDUE_QUERY }]
    });
  }
}
