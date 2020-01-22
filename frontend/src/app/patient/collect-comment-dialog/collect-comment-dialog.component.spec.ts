import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CollectCommentDialogComponent } from './collect-comment-dialog.component';

describe('CollectCommentDialogComponent', () => {
  let component: CollectCommentDialogComponent;
  let fixture: ComponentFixture<CollectCommentDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CollectCommentDialogComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CollectCommentDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
