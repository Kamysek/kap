import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WeekSwitcherComponent } from './week-switcher.component';

describe('WeekSwitcherComponent', () => {
  let component: WeekSwitcherComponent;
  let fixture: ComponentFixture<WeekSwitcherComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [WeekSwitcherComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WeekSwitcherComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
