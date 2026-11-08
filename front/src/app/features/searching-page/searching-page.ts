import {
  Component,
  ChangeDetectionStrategy,
  OnInit,
  inject,
  WritableSignal,
  signal,
} from '@angular/core';
import { SearchService } from '../../services/search-service';
import { ActivatedRoute } from '@angular/router';
import { SearchResult } from '../../models/search-result';
import { LoaderService } from '../../services/loader-service';
import { SearchBar } from '../../shared/search-bar/search-bar';

@Component({
  selector: 'app-searching-page',
  imports: [SearchBar],
  templateUrl: './searching-page.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrl: './searching-page.scss',
})
export class SearchingPage implements OnInit {
  private service: SearchService = inject(SearchService);
  private loaderService: LoaderService = inject(LoaderService);
  private route: ActivatedRoute = inject(ActivatedRoute);
  private result: WritableSignal<SearchResult | null> = signal(null);

  public get Result() {
    return this.result.asReadonly();
  }

  ngOnInit() {
    this.route.queryParams.subscribe((params) => {
      this.service.search(params['query']).subscribe({
        next: (result) => {
          this.result.set(result);
        },
        error: (err) => console.error(err),
      });
    });
  }
}
