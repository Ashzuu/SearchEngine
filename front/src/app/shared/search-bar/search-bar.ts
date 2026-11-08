import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgIcon } from '@ng-icons/core';
import { ActivatedRoute } from '@angular/router';
import { SearchBarService } from '../../services/search-bar-service';

@Component({
  imports: [FormsModule, NgIcon],
  selector: 'app-search-bar',
  styleUrl: './search-bar.scss',
  templateUrl: './search-bar.html',
})
export class SearchBar implements OnInit {
  private searchBarService: SearchBarService = inject(SearchBarService);
  private route: ActivatedRoute | null = inject(ActivatedRoute, { optional: true });

  public get Value(): string {
    return this.searchBarService.Value;
  }

  public set Value(val: string) {
    this.searchBarService.Value = val;
  }

  ngOnInit(): void {
    this.route?.queryParams.subscribe((params) => {
      if (params['query']) {
        this.searchBarService.setValue(params['query']);
      }
    });
  }

  onClickEnter(event: KeyboardEvent, query: string): void {
    if (event.key === 'Enter') {
      this.sendData(query);
    }
  }

  sendData(query: string): void {
    this.searchBarService.sendData(query);
  }
}
