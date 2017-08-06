import { AuthService } from './auth.service';
import { JwtHelper } from 'angular2-jwt';
import { Observable } from 'rxjs/Observable';
import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';

@Injectable()
export class JwtExpiredInterceptor implements HttpInterceptor{
    /*
    HTTP Interceptor that blocks the requests and logout the user if the jwt token has expired
    But seems like angular2-jwt AuthHttp doesn't support Http Interceptors yet.
    https://github.com/auth0/angular2-jwt/issues/383
    */
    
    jwtHelper: JwtHelper = new JwtHelper();

    constructor(private authService: AuthService){}
    
    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        let token = this.authService.getToken()
        if(this.jwtHelper.isTokenExpired(token)){
            this.authService.logout()
            return Observable.empty()
        }
        return next.handle(req);
    }
}