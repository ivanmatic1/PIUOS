import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef  } from '@angular/material/dialog';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders, HttpClientModule  } from '@angular/common/http';
import { ActivatedRoute, Router  } from '@angular/router';

@Component({
  selector: 'app-edit-personal-information',
  standalone: true,
  imports: [HttpClientModule, FormsModule],
  templateUrl: './edit-personal-information.component.html',
  styleUrl: './edit-personal-information.component.css'
})
export class EditPersonalInformationComponent {

  username: string = '';
  firstname: string = '';
  lastname: string = '';

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<EditPersonalInformationComponent>,
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.username = data.username;
    this.firstname = data.firstname;
    this.lastname = data.lastname;
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
      username: this.username,
      first_name: this.firstname,
      last_name: this.lastname
    };

    const url = `http://127.0.0.1:8000/api/account/profile/`

    this.http.patch(url, payload, { headers }).subscribe(
      (res: any) => {
        if (res) {
          alert('Profile updated successfully!');
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

