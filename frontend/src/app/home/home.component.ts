import { Component, OnInit } from '@angular/core';
import { BlogService } from '../services/blog.service';
import { NgIf, NgFor } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [NgIf, NgFor],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {
  blogs: any[] = [];

  constructor(private blogService: BlogService, private router: Router) { }

  ngOnInit(): void {
    this.fetchBlogs();
  }

  fetchBlogs(): void {
    this.blogService.getBlogs().subscribe(response => {
      this.blogs = response.data;
    });
  }

  redirectToBlog(blogId: number): void {
    this.router.navigate(['/blog', blogId]);
  }
}
