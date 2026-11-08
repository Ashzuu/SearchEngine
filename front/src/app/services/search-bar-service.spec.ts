import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { SearchBarService } from './search-bar-service';

describe('SearchBarService', () => {
  let service: SearchBarService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideRouter([])],
    });
    service = TestBed.inject(SearchBarService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should update and get value', () => {
    service.Value = 'test';
    expect(service.Value).toBe('test');
  });
});
