import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class BlogService {
  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  getBlogs(): Observable<any> {
    // Retrieve the token from localStorage
    const token: string | null = localStorage.getItem('loginToken');

    // Include the token in the HTTP headers
    const headers = new HttpHeaders({
      'Authorization': token ? `Bearer ${token}` : ''
    });

    // Make the GET request with authentication headers
    return this.http.get<any>(`${this.apiUrl}/`, { headers });
  }
}