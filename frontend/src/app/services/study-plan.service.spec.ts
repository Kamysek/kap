import { TestBed } from '@angular/core/testing';

import { StudyPlanService } from './study-plan.service';

describe('StudyPlanService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: StudyPlanService = TestBed.get(StudyPlanService);
    expect(service).toBeTruthy();
  });
});
