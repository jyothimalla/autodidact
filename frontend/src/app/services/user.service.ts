import { Injectable } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';



interface UserProfile {
  username: string;
  awarded_title?: string;
  ninja_stars?: number;
  progress?: any[];
  user_id: 0;
}



@Injectable({ providedIn: 'root' })
export class UserService {

  get username(): string {

    return localStorage.getItem('username') || 'Guest';;
  }

  get user_id(): number {
    return parseInt(localStorage.getItem('user_id') || '0', 10);
  }

  get isLoggedIn(): boolean {
    return this.username !== 'Guest' && this.user_id > 0;
  }

  get isGuest(): boolean {
    return this.username === 'Guest' || this.user_id === 0;
  }

  setUser(username: string, userId: number): void {
    localStorage.setItem('username', username);
    localStorage.setItem('user_id', userId.toString());
  }

  clearUser(): void {
    localStorage.removeItem('username');
    localStorage.removeItem('user_id');
  }

  loadGuestUser(): void {
    this.setUser('Guest', 0);
  }
}
