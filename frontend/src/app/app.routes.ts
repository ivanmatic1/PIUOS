import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { CreateblogComponent } from './createblog/createblog.component';

export const routes: Routes = [
    {
        path: 'login', 
        component:LoginComponent
    },
    {
        path: 'register', 
        component:RegisterComponent
    },
    {
        path: '', 
        component:HomeComponent,
    },
    {
        path: 'create',
        component: CreateblogComponent
    },
];

