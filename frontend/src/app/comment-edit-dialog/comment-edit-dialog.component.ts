import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef  } from '@angular/material/dialog';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders, HttpClientModule  } from '@angular/common/http';
import { ActivatedRoute, Router  } from '@angular/router';


@Component({
  selector: 'app-comment-dialog',
  standalone: true,
  imports: [HttpClientModule, FormsModule],
  templateUrl: './comment-edit-dialog.component.html',
  styleUrl: './comment-edit-dialog.component.css'
})

export class CommentEditDialogComponent {
  commentText: string = '';

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<CommentEditDialogComponent>,
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.commentText = data.commentText;
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
      comment_text: this.commentText
    };

    const commentId = this.data.commentId; // Access the commentId from the data object

    this.http.patch(`http://127.0.0.1:8000/comments/${commentId}/`, payload, { headers }).subscribe(
      (res: any) => {
        if (res) {
          alert('Comment updated successfully!');
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

  cancel(): void {
    this.dialogRef.close();
  }

  reloadCurrentRoute() {
    const currentUrl = this.router.url;
    this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
      this.router.navigate([currentUrl]); // Navigate to the current URL
  });
  }

}