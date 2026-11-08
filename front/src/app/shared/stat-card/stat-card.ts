import { Component, Input, Signal, signal, WritableSignal } from '@angular/core';

@Component({
  imports: [],
  selector: 'app-stat-card',
  styleUrl: './stat-card.scss',
  templateUrl: './stat-card.html',
})
export class StatCard {
  private title: WritableSignal<string> = signal('');
  private littleDescription: WritableSignal<string> = signal('');

  public get Title(): Signal<string> {
    return this.title.asReadonly();
  }

  public get LittleDescription(): Signal<string> {
    return this.littleDescription.asReadonly();
  }

  @Input({ required: true })
  public set Title(title: string) {
    this.title.set(title);
  }

  @Input({ required: false })
  public set LittleDescription(value: string) {
    this.littleDescription.set(value);
  }
}
