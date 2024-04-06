import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { CreateblogComponent } from './createblog/createblog.component';
import { BlogComponent } from './blog/blog.component';
import { ViewPersonalInformationComponent } from './view-personal-information/view-personal-information.component';
import { ViewProfileComponent } from './view-profile/view-profile.component';
import { SearchComponent } from './search/search.component';
import { FilterComponent } from './filter/filter.component';

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
    {
        path: 'profile',
        component: ViewPersonalInformationComponent
    },
    {
        path: 'user/:username',
        component: ViewProfileComponent
    },
    {
        path: 'blog/:id',
        component: BlogComponent
    },
    { 
        path: 'search/:query',
        component: SearchComponent 
    },
    { 
        path: 'filter/:category',
        component: FilterComponent 
    },
];

