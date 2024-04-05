
import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-view-profile',
  standalone: true,
  imports: [],
  templateUrl: './view-profile.component.html',
  styleUrl: './view-profile.component.css'
})

export class ViewProfileComponent implements OnInit {
  username: string = ''; // Initialize username property

  firstname: string = '';
  lastname: string = '';

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    // Subscribe to the route parameter changes to get the username from the URL
    this.route.paramMap.subscribe(params => {
      const usernameFromUrl = params.get('username');
      if (usernameFromUrl) {
        this.username = usernameFromUrl;
        this.fetchUserProfile(usernameFromUrl); // Fetch user profile based on the obtained username
      }
    });
  }

  fetchUserProfile(username: string): void {
    const token: string | null = localStorage.getItem('loginToken');

    // Include the token in the HTTP headers
    const headers = new HttpHeaders({
      'Authorization': token ? `Bearer ${token}` : ' ' // Include empty token if no token found
    });

    const url = `http://127.0.0.1:8000/api/account/user/?username=${username}`;
    this.http.get(url, { headers }).subscribe(
      (response: any) => {
        if (response.data && response.data.length > 0) {
          const userData = response.data[0]; // Get the first user data object
          this.firstname = userData.first_name;
          this.lastname = userData.last_name;
        } else {
          console.error('No user data found');
        }
      },
      (error) => {
        console.error('Error fetching user profile:', error);
      }
    );
    
  }
}

