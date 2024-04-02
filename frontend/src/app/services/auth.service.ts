import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  private isLoggedIn = new BehaviorSubject<boolean>(false);
  private username = new BehaviorSubject<string>('');

  constructor() { }

  isAuthenticated(): Observable<boolean> {
    return this.isLoggedIn.asObservable();
  }
  
  getUsername(): Observable<string> {
    return this.username.asObservable();
  }

 login(username: string): void {
    this.isLoggedIn.next(true);
    this.username.next(username);
  }

  logout(): void {
    this.isLoggedIn.next(false);
    this.username.next('');
  }
}