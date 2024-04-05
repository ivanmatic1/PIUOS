import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { EditPersonalInformationComponent } from '../edit-personal-information/edit-personal-information.component'
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-view-personal-information',
  standalone: true,
  imports: [],
  templateUrl: './view-personal-information.component.html',
  styleUrl: './view-personal-information.component.css'
})

export class ViewPersonalInformationComponent {
  isAuthenticated = false;
  loggedInUser: string | null = null;
  username: string = '';
  firstname: string = '';
  lastname: string = '';

  constructor(
    private authService: AuthService,
    private http: HttpClient,
    public dialog: MatDialog
  ) { }


  ngOnInit(): void {
    this.authService.isAuthenticated().subscribe(isAuthenticated => {
      this.isAuthenticated = isAuthenticated;
    });

    this.authService.getUsername().subscribe(username => {
      this.loggedInUser = username;
    });

    const token: string | null = localStorage.getItem('loginToken');
  
    if (!token) {
      console.error('Token is missing!');
      return;
    }

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });

    const url = 'http://127.0.0.1:8000/api/account/profile/'
    this.http.get(url,{headers}).subscribe(
      (response: any) => {
        this.username = response.username;
        this.firstname = response.first_name;
        this.lastname = response.last_name;
      },
    );
  }

  openEditProfile() {
    const dialogRef = this.dialog.open(EditPersonalInformationComponent, {
      width: '350px',
      data: {
        username: this.username ,
        firstname: this.firstname,
        lastname: this.lastname,
      }
    });
  
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }

}
