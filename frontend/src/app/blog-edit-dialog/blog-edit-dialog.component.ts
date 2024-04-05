import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef  } from '@angular/material/dialog';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders, HttpClientModule  } from '@angular/common/http';
import { ActivatedRoute, Router  } from '@angular/router';

@Component({
  selector: 'app-blog-edit-dialog',
  standalone: true,
  imports: [HttpClientModule, FormsModule],
  templateUrl: './blog-edit-dialog.component.html',
  styleUrl: './blog-edit-dialog.component.css'
})
export class BlogEditDialogComponent {
  blogText: string = '';
  blogTitle: string = '';
  blogCategory: string = '';
  blogId: number = 0;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<BlogEditDialogComponent>,
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.blogText = data.blogText;
    this.blogTitle = data.blogTitle;
    this.blogCategory = data.blogCategory;
    this.blogId = data.blogId;
  }

  cancel(): void {
    this.dialogRef.close();
  }

  onSubmit() {
    const token: string | null = localStorage.getItem('loginToken');

    if (!token) {
      console.error('Token is missing!');
      return;
    }

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });

    const payload = {
      id: this.blogId,
      title: this.blogTitle,
      blog_text: this.blogText,
      category: this.blogCategory
    };

    const url = `http://127.0.0.1:8000/blog/`

    this.http.patch(url, payload, { headers }).subscribe(
      (res: any) => {
        if (res) {
          alert('Blog updated successfully!');
          this.dialogRef.close();
          this.reloadCurrentRoute();
        } else {
          alert('Failed to update comment');
        }
      },
      (error) => {
        console.error('Error updating comment:', error);
        alert('Failed to update comment');
      }
    );
  }

  reloadCurrentRoute() {
    const currentUrl = this.router.url;
    this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
      this.router.navigate([currentUrl]); // Navigate to the current URL
  });
  }
}
