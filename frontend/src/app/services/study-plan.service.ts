import { Injectable } from '@angular/core';
import { Apollo } from 'apollo-angular';
import gql from 'graphql-tag';
import { getStudies } from '../../../__generated__/getStudies';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class StudyPlanService {
  private static GTE_STUDIES = gql`
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

  constructor(private apollo: Apollo) {}

  getPlans() {
    return this.apollo
      .watchQuery<getStudies>({ query: StudyPlanService.GTE_STUDIES })
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
}
