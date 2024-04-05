import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef  } from '@angular/material/dialog';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders, HttpClientModule  } from '@angular/common/http';
import { ActivatedRoute, Router  } from '@angular/router';


@Component({
  selector: 'app-comment-dialog',
  standalone: true,
  imports: [HttpClientModule, FormsModule],
  templateUrl: './comment-dialog.component.html',
  styleUrl: './comment-dialog.component.css'
})

export class CommentDialogComponent {
  commentText: string = '';

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<CommentDialogComponent>, // Inject MatDialogRef
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router
  ) {}

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
      comment_text: this.commentText, // Include the comment text in the payload
      blog: this.data.blogId // Use this.data.blogId to access the blogId passed from BlogComponent
    };

    this.http.post('http://127.0.0.1:8000/comments/', payload, { headers }).subscribe((res: any) => {
      if (res) {
        alert('Comment added!');
        this.reloadCurrentRoute();
      } else {
        alert(res.message);
      }
    });

    this.dialogRef.close(); // Close the dialog after submitting
  }

  reloadCurrentRoute() {
    const currentUrl = this.router.url;
    this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
      this.router.navigate([currentUrl]); // Navigate to the current URL
  });
  }
}