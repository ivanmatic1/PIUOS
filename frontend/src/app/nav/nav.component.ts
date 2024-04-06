import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router, RouterOutlet, RouterLink, RouterLinkActive} from '@angular/router';
import { NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Import FormsModule

@Component({
  selector: 'app-nav',
  standalone: true,
  imports: [NgIf, RouterOutlet, RouterLink, RouterLinkActive, FormsModule],
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css'],
})

export class NavComponent implements OnInit {
  isAuthenticated: boolean = false;
  username: string = '';
  dropdownOpen: boolean = false;
  query: string = '';
  

  constructor(private authService: AuthService, private router: Router) { }

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
  

  search(): void {
    if (this.query.trim() !== '') {
      this.router.navigate(['/search/'+this.query]);
    }
  }

  logout(): void {
    this.authService.logout();
  }
}
