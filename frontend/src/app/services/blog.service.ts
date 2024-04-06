import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams  } from '@angular/common/http';
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
      'Authorization': token ? `Bearer ${token}` : ' ' // Include empty token if no token found
    });

    return this.http.get<any>(`${this.apiUrl}/`, { headers });
  }

  searchBlogs(query: string): Observable<any> {
    const token: string | null = localStorage.getItem('loginToken');
    const headers = new HttpHeaders({
      'Authorization': token ? `Bearer ${token}` : ''
    });

    const url = `${this.apiUrl}/?search=${query}`;

    return this.http.get<any>(url, { headers });
  }

  getUnauthenticatedBlogDetails(blogId: number): Observable<any> {
    const url = `${this.apiUrl}/blog/${blogId}/`;
    return this.http.get<any>(url);
  }

  getAuthenticatedBlogDetails(blogId: number): Observable<any> {
    const url = `${this.apiUrl}/blog_logged/${blogId}/`;
    return this.http.get<any>(url);
  }
  
}
