import { HttpClient } from '@angular/common/http';
import { Component, NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Routes, Router, RouterOutlet, RouterLink, RouterLinkActive} from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {

  loginObj: any = {
    "username": "",
    "password": ""
  };

  constructor(private http: HttpClient, private router: Router){}

  onLogin(){
    this.http.post('http://127.0.0.1:8000/api/account/login/', this.loginObj).subscribe((res:any)=>{
      if(res.result){
        localStorage.setItem('loginToken', res.data.token.access);
        this.router.navigate(['http://localhost:4200/']);
      }else{
        alert(res.message);
      }
    })
  }
}
