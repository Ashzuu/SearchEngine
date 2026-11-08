import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { lucideSearch } from '@ng-icons/lucide';

import { routes } from './app.routes';
import { provideIcons } from '@ng-icons/core';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideIcons({ lucideSearch })
  ]
};
