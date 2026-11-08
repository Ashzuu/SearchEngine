import {
  Component,
  ChangeDetectionStrategy,
  inject,
  WritableSignal,
  signal,
  OnInit,
  Optional,
  Signal,
} from '@angular/core';
import { NgIcon } from '@ng-icons/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { SearchBar } from '../../shared/search-bar/search-bar';
import { SearchService } from '../../services/search-service';
import { StatResult } from '../../models/stat-result';
import { StatCard } from '../../shared/stat-card/stat-card';

@Component({
  selector: 'app-home-page',
  imports: [FormsModule, SearchBar, StatCard],
  templateUrl: './home-page.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrl: './home-page.scss',
})
export class HomePage implements OnInit {
  private service: SearchService = inject(SearchService);
  private result: WritableSignal<StatResult | null> = signal<StatResult | null>(null);

  public get Result(): Signal<StatResult | null> {
    return this.result?.asReadonly();
  }

  ngOnInit() {
    this.service.stats().subscribe((result) => {
      this.result.set(result);
    });
  }
}
