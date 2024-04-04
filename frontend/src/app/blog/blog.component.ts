import { Component, OnInit } from '@angular/core';
import { BlogService } from '../services/blog.service';
import { ActivatedRoute } from '@angular/router'; 
import { AuthService } from '../services/auth.service';
import { NgIf, NgFor } from '@angular/common';
import { HttpClient, HttpHeaders, HttpClientModule  } from '@angular/common/http';

@Component({
  selector: 'app-blog',
  standalone: true,
  imports: [NgIf, HttpClientModule, NgFor],
  templateUrl: './blog.component.html',
  styleUrl: './blog.component.css'
})

export class BlogComponent implements OnInit {
  blog: any;
  comments: any[] = [];
  isAuthenticated = false;
  userLikeChoice: string | undefined;

  constructor(
    private route: ActivatedRoute,
    private blogService: BlogService,
    private authService: AuthService,
    private http: HttpClient
  ) { }

  ngOnInit(): void {

    this.route.paramMap.subscribe(params => {
      this.fetchBlogDetails(params);
    });

    this.authService.isAuthenticated().subscribe(isAuthenticated => {
      this.isAuthenticated = isAuthenticated;
    });
  }

  fetchBlogDetails(params: any): void {
    const idParam = params.get('id');

    if (idParam !== null && !isNaN(+idParam)) {
      const blogId = +idParam;
      this.blogService.getBlogById(blogId).subscribe(
        (data: any) => {
          this.blog = data.blog;
          this.userLikeChoice = data.blog.likes.user_like_choice;
          this.comments = data.comments;
        },
        (error) => {
          console.error('Error fetching blog details:', error);
        }
      );
    } else {
      alert('Wrong id!')
    }
  }

  likePost() {
    const token: string | null = localStorage.getItem('loginToken');
  
    if (!token) {
      console.error('Token is missing!');
      return;
    }
  
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
  
    const url = 'http://127.0.0.1:8000/blog/' + this.blog.id + '/like/';
    const payload = {
      like_choice: 'like'
    };
  
    this.http.post(url, payload, { headers }).subscribe(
      (response: any) => {
        this.userLikeChoice = 'like'; // Ensure that this assignment is correct
        this.fetchBlogDetails(this.route.snapshot.paramMap);
      },
    );
  }

  dislikePost() {
    const token: string | null = localStorage.getItem('loginToken');
  
    if (!token) {
      console.error('Token is missing!');
      return;
    }
  
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
  
    const url = 'http://127.0.0.1:8000/blog/' + this.blog.id + '/like/';
    const payload = {
      like_choice: 'dislike'
    };
  
    this.http.post(url, payload, { headers }).subscribe(
      (response: any) => {
        this.userLikeChoice = 'dislike'; // Ensure that this assignment is correct
        this.fetchBlogDetails(this.route.snapshot.paramMap);
      },
    );
  }
}