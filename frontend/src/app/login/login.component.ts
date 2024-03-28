import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [HttpClientModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {

  loginObj: Login;


  constructor(private http: HttpClient, private router: Router, private authService: AuthService){
    this.loginObj = new Login();
  }

  onLogin() {
    this.http.post('http://127.0.0.1:8000/api/account/login/', this.loginObj).subscribe((res: any) => {
      if (res) {
        localStorage.setItem('loginToken', res.data.token.access);
  
        this.authService.login(this.loginObj.username); 
        
        this.router.navigate(['/']);
      } else {
        alert(res.message);
      }
    })
  }
}

export class Login{
  username: string;
  password: string;
  constructor(){
    this.username = '';
    this.password = '';
    }
}
