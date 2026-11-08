import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { SearchResult } from '../models/search-result';
import { StatResult } from '../models/stat-result';

@Injectable({
  providedIn: 'root',
})
export class SearchService {
  private client:HttpClient = inject(HttpClient);
  private url: string = environment.baseUrl;

  public search(query: string){
    return this.client.get<SearchResult>(this.url + 'search?query=' + query)
  }

  public stats(){
    return this.client.get<StatResult>(this.url + 'stats');
  }
}
