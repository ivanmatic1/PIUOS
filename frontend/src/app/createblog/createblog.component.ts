import { HttpClient, HttpHeaders, HttpClientModule  } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-createblog',
  standalone: true,
  imports: [HttpClientModule, FormsModule],
  templateUrl: './createblog.component.html',
  styleUrl: './createblog.component.css'
})

export class CreateblogComponent {
  blogData = {
    title: '',
    blog_text: '',
    category: '',
    comments: []
  };

  constructor(private http: HttpClient, private router: Router) { }

  onSubmit() {
    // Retrieve the token from localStorage
    const token: string | null = localStorage.getItem('loginToken');

    // Check if the token exists
    if (!token) {
      // Handle the case where the token is missing
      console.error('Token is missing!');
      return;
    }

    // Include the token in the HTTP headers
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });

    // Make the POST request with authentication headers
    this.http.post('http://127.0.0.1:8000/blog/', this.blogData, { headers }).subscribe((res: any) => {
      if (res) {
        alert(res.message);
        this.router.navigate(['/']);
      } else {
        alert(res.message);
      }
    });
  }
}