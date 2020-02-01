import { Injectable } from '@angular/core';
import { Apollo } from 'apollo-angular';
import gql from 'graphql-tag';
import { getStudies } from '../../../__generated__/getStudies';
import { map } from 'rxjs/operators';
import {
  CreateCheckupInput,
  DeleteCheckupInput
} from '../../../__generated__/globalTypes';
import {
  createCheckup,
  createCheckupVariables
} from '../../../__generated__/createCheckup';
import {
  deleteCheckup,
  deleteCheckupVariables
} from '../../../__generated__/deleteCheckup';

@Injectable({
  providedIn: 'root'
})
export class StudyPlanService {
  private static GET_STUDIES = gql`
    query getStudies {
      getStudies {
        edges {
          node {
            id
            name
            checkupSet {
              edges {
                node {
                  id
                  name
                  daysUntil
                }
              }
            }
          }
        }
      }
    }
  `;

  private static CREATE_CHECKUP = gql`
    mutation createCheckup($checkupInput: CreateCheckupInput!) {
      createCheckup(input: $checkupInput) {
        checkup {
          id
          daysUntil
        }
      }
    }
  `;

  private static DELETE_CHECKUP = gql`
    mutation deleteCheckup($checkupInput: DeleteCheckupInput!) {
      deleteCheckup(input: $checkupInput) {
        ok
      }
    }
  `;

  constructor(private apollo: Apollo) {}

  getPlans() {
    return this.apollo
      .watchQuery<getStudies>({ query: StudyPlanService.GET_STUDIES })
      .valueChanges.pipe(
        map(res =>
          res.data.getStudies.edges.map(studyEdge =>
            Object.assign({}, studyEdge.node, {
              checkups: studyEdge.node.checkupSet.edges.map(
                checkupEdge => checkupEdge.node
              )
            })
          )
        )
      );
  }

  createCheckup(checkupInput: CreateCheckupInput) {
    return this.apollo.mutate<createCheckup, createCheckupVariables>({
      mutation: StudyPlanService.CREATE_CHECKUP,
      variables: { checkupInput },
      refetchQueries: [{ query: StudyPlanService.GET_STUDIES }]
    });
  }

  deleteCheckup(checkupInput: DeleteCheckupInput) {
    return this.apollo.mutate<deleteCheckup, deleteCheckupVariables>({
      mutation: StudyPlanService.DELETE_CHECKUP,
      variables: { checkupInput },
      refetchQueries: [{ query: StudyPlanService.GET_STUDIES }]
    });
  }
}
