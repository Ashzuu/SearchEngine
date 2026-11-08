import { Routes } from '@angular/router';
import { HomePage } from './features/home-page/home-page';
import { SearchingPage } from './features/searching-page/searching-page';

export const routes: Routes = [
  {
    path: '',
    component: HomePage
  },
  {
    path: 'search',
    component: SearchingPage
  }
];
