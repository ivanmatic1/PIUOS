import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';

@Injectable()
export class CustomInterceptor implements HttpInterceptor {
  constructor(){}
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
      const token = localStorage.getItem('loginToken')
      const newCloneRequest = req.clone({
        setHeaders:{
          Autherization: `Bearer ${token}`
        }
      })
      return next.handle(req);
  }
}
