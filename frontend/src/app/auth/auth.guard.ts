import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const authGuard: CanActivateFn = () => {
  const router = inject(Router);
  const user = localStorage.getItem('username');
  if (!user) {
    router.navigate(['/login']);
    return false;
  }
  return true;
};
