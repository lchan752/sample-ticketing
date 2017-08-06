import { environment } from './../../../environments/environment';
import { AuthHttp, JwtHelper } from 'angular2-jwt';
import { AuthenticatedUser } from './../models/auth-user';
import { Injectable } from '@angular/core'
import { BehaviorSubject, Subject } from 'rxjs/Rx';
import { Observable } from 'rxjs/Observable';
import { ToasterService, Toast } from 'angular2-toaster';

@Injectable()
export class AuthService{
    authenticatedUser: BehaviorSubject<AuthenticatedUser> = new BehaviorSubject<AuthenticatedUser>(null)
    jwtHelper: JwtHelper = new JwtHelper();


    constructor(
        private authHttp: AuthHttp,
        private toaster: ToasterService,
    ){
        let token = this.getToken()
        if(token == null){
            return
        }else if(this.jwtHelper.isTokenExpired(token)){
            this.clearToken()
            this.clearUser()
            this.authenticatedUser.next(null)
        }else{
            let user = this.getUser()
            this.authenticatedUser.next(user)
        }
    }

    getToken(): string{
        return localStorage.getItem('token')
    }

    getUser(): AuthenticatedUser{
        let json = localStorage.getItem('currentUser')
        if(json == null){
            return null
        }
        let dt = JSON.parse(localStorage.currentUser)
        return new AuthenticatedUser(dt.userId, dt.name, dt.avatar, dt.isManager)
    }

    saveToken(token: string){
        if(token){
            localStorage.setItem('token', token)
        }
    }

    saveUser(user: AuthenticatedUser){
        if(user){
            localStorage.setItem('currentUser', JSON.stringify(user))
        }
    }

    clearToken(){
        localStorage.removeItem('token')
    }

    clearUser(){
        localStorage.removeItem('currentUser')
    }

    login(email: string, password: string){
        let postData = {
            email: email,
            password: password
        }
        this.authHttp.post(environment.api_root + '/api-token-auth/', postData).subscribe(
            data => {
                let resp = data.json()
                this.saveToken(resp.token)
                let user = new AuthenticatedUser(
                    resp.user.id,
                    resp.user.full_name,
                    resp.user.avatar,
                    resp.user.is_manager,
                )
                this.saveUser(user)
                this.authenticatedUser.next(user)
                this.toaster.pop("success", "You are now logged in.");
            },
            err => {
                let resp = err.json()
                let errors = resp.non_field_errors;
                this.toaster.pop("error", errors);
            }
        )
    }

    logout(){
        this.clearToken()
        this.clearUser()
        this.authenticatedUser.next(null)
        this.toaster.pop("success", "You are now logged out.")
    }
}