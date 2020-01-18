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
          }
        }
      }
    }
  `;

  private static LOAD_USER_DETAILS = gql`
    query getUserDetails {
      getMe {
        id
        username
        dateJoined
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

  constructor(private apollo: Apollo) {}

  getUsers() {
    return this.apollo
      .watchQuery<getUsers>({ query: UserService.LOAD_USERS_QUERY })
      .valueChanges.pipe(
        map(res => res.data.getUsers.edges.map(edge => edge.node))
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
}
