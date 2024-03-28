import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router, RouterOutlet, RouterLink, RouterLinkActive} from '@angular/router';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-nav',
  standalone: true,
  imports: [NgIf, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css'],
})

export class NavComponent implements OnInit {
  isAuthenticated: boolean = false;
  username: string = '';
  dropdownOpen: boolean = false;

  constructor(private authService: AuthService) { }

  ngOnInit(): void {
    this.authService.isAuthenticated().subscribe((authenticated: boolean) => {
      this.isAuthenticated = authenticated;
    });

    this.authService.getUsername().subscribe((username: string) => {
      this.username = username;
    });
    
  }

  toggleDropdown() {
    this.dropdownOpen = !this.dropdownOpen;
  }

  closeDropdown() {
    this.dropdownOpen = false;
  }
  

  logout(): void {
    this.authService.logout();
  }
}
