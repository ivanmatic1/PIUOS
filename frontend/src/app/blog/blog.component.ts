import { Component, OnInit } from '@angular/core';
import { BlogService } from '../services/blog.service';
import { ActivatedRoute } from '@angular/router'; 


@Component({
  selector: 'app-blog',
  standalone: true,
  imports: [],
  templateUrl: './blog.component.html',
  styleUrl: './blog.component.css'
})

export class BlogComponent implements OnInit {
  blog: any;

  constructor(private route: ActivatedRoute,
              private blogService: BlogService) { }

  ngOnInit(): void {
    // Subscribe to changes in route parameters
    this.route.paramMap.subscribe(params => {
      const idParam = params.get('id');
      
      // Check if idParam is not null and is a valid number
      if (idParam !== null && !isNaN(+idParam)) {
        const blogId = +idParam; 

        alert(blogId)
        this.blogService.getBlogById(blogId).subscribe(
          (data: any) => {
            this.blog = data;
          },
          (error) => {
            console.error('Error fetching blog details:', error);
          }
        );
      } else {
        console.error('Invalid blog ID:', idParam);
      }
    });
  }
}