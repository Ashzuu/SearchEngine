import { inject, Injectable, signal, WritableSignal } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class SearchBarService {
  private router: Router = inject(Router);
  private value: WritableSignal<string> = signal('');

  public get Value(): string {
    return this.value();
  }

  public set Value(val: string) {
    this.value.set(val);
  }

  public setValue(val: string): void {
    this.value.set(val);
  }

  public sendData(query?: string): void {
    const q = (query !== undefined ? query : this.value()).trim();
    if (q) {
      this.value.set(q);
      this.router.navigate(['/search'], { queryParams: { query: q } });
    }
  }
}
