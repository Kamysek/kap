import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewCalendarDialogComponent } from './new-calendar-dialog.component';

describe('NewCalendarDialogComponent', () => {
  let component: NewCalendarDialogComponent;
  let fixture: ComponentFixture<NewCalendarDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewCalendarDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewCalendarDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
