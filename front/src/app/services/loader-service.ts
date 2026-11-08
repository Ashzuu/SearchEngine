import { computed, Service, signal, Signal, WritableSignal } from '@angular/core';

@Service()
export class LoaderService {
  private counterLoader: WritableSignal<number> = signal(0);
  private isLoading: Signal<boolean> = computed(() => this.counterLoader() > 0);

  public get IsLoading(): Signal<boolean>{
    return this.isLoading;
  }

  public addElement(): void {
    return this.counterLoader.update((value) => value + 1);
  }

  public removeElement(): void {
    return this.counterLoader.update((value) => value - 1);
  }
}
