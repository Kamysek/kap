import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OverduePatientsComponent } from './overdue-patients.component';

describe('OverduePatientsComponent', () => {
  let component: OverduePatientsComponent;
  let fixture: ComponentFixture<OverduePatientsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [OverduePatientsComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OverduePatientsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
