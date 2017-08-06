import { Router } from '@angular/router';
import { AuthService } from './../../auth/services/auth.service';
import { Component, OnInit } from '@angular/core'


@Component({
    templateUrl: './login.html',
    styleUrls: ['./login.css'],
})
export class Login implements OnInit{
    email: string
    password: string
    
    constructor(private authService: AuthService, private router: Router){}

    ngOnInit(){
        this.authService.authenticatedUser.subscribe((user)=>{
            if(user == null){
                return
            }else if(user.isManager){
                this.router.navigate(['manager-tickets'])
            }else{
                this.router.navigate(['worker-tickets'])
            }
        })
    }

    login(){
        this.authService.login(this.email, this.password)
    }
}