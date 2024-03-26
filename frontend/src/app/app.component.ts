import { Component, NgModule } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive} from '@angular/router';
import { NavComponent } from './nav/nav.component';
import { FormsModule } from '@angular/forms';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { CustomInterceptor } from './services/custom.interceptor';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavComponent, RouterLink, RouterLinkActive, FormsModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  providers:[
    {
      provide: HTTP_INTERCEPTORS,
      useClass: CustomInterceptor,
      multi:true
    }
  ], 
  
})
export class AppComponent {
  title = 'frontend';
}
