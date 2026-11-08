import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchingPage } from './searching-page';

describe('SearchingPage', () => {
  let component: SearchingPage;
  let fixture: ComponentFixture<SearchingPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SearchingPage],
    }).compileComponents();

    fixture = TestBed.createComponent(SearchingPage);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
