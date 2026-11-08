import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { LoaderService } from '../services/loader-service';
import { finalize } from 'rxjs';

export const httpInterceptorInterceptor: HttpInterceptorFn = (req, next) => {
  const loaderService:LoaderService = inject(LoaderService);
  loaderService.addElement();

  return next(req).pipe(
    finalize(() => loaderService.removeElement())
  );
};
