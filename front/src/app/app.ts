import { Component, signal, ChangeDetectionStrategy } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { BaseLayout } from './layout/base-layout/base-layout';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, BaseLayout],
  templateUrl: './app.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('front');
}
