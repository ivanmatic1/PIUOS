import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router  } from '@angular/router';
import { BlogService } from '../services/blog.service';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [NgFor],
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})

export class SearchComponent implements OnInit {
  query: string = '';
  blogs: any[] = [];

  constructor(private route: ActivatedRoute, private blogService: BlogService, private router: Router) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.query = params['query'];
      this.searchBlogs(this.query);
    });
  }

  searchBlogs(query: string): void {
    if (query.trim() !== '') {
      this.blogService.searchBlogs(query).subscribe(response => {
        this.blogs = response.data; // Assuming the response contains a 'data' property with search results
      });
    }
  }

  redirectToBlog(blogId: number): void {
    this.router.navigate(['/blog', blogId]);
  }
}