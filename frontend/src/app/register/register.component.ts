import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { Component, NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router} from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, HttpClientModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {

  registerObj: Register;


  constructor(private http: HttpClient, private router: Router){
    this.registerObj = new Register();
  }

  onRegister(){
    this.http.post('http://127.0.0.1:8000/api/account/register/', this.registerObj).subscribe((res:any)=>{
      if(res){
        alert(res.message);
        this.router.navigate(['/']);
      }else{
        alert(res.data.non_field_errors);
      }
    })
  }
}

export class Register{
  first_name: string;
  last_name: string;
  username: string;
  password: string;
  constructor(){
    this.first_name = '';
    this.last_name = '';
    this.username = '';
    this.password = '';
    }
}