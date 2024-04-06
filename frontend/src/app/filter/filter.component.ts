import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router  } from '@angular/router';
import { BlogService } from '../services/blog.service';
import { NgFor } from '@angular/common';


@Component({
  selector: 'app-filter',
  standalone: true,
  imports: [NgFor],
  templateUrl: './filter.component.html',
  styleUrl: './filter.component.css'
})
export class FilterComponent implements OnInit {
  category: string = '';
  blogs: any[] = [];

  constructor(private route: ActivatedRoute, private blogService: BlogService, private router: Router) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.category = params['category']; // Retrieve the category from route parameters
      this.filterBlogsByCategory(this.category);
    });
  }

  filterBlogsByCategory(query: string): void {
    this.blogService.filterBlog(query).subscribe(response => {
      this.blogs = response.data;
    });
  }

  redirectToBlog(blogId: number): void {
    this.router.navigate(['/blog', blogId]);
  }
}