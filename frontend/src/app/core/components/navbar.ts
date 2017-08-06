import { AuthService } from './../../auth/services/auth.service';
import { AuthenticatedUser } from './../../auth/models/auth-user';
import { Component, OnInit } from '@angular/core';
@Component({
    selector: 'navbar',
    templateUrl: './navbar.html',
    styleUrls: ['./navbar.css'],
})
export class Navbar implements OnInit{
    authUser: AuthenticatedUser = null;

    constructor(private authService: AuthService){}

    ngOnInit(){
        this.authService.authenticatedUser.subscribe((user)=>{
            this.authUser = user
        })
    }

    isAuthenticated():boolean{
        return this.authUser != null;
    }

    ticketsLink():string{
        return this.authUser.isManager ? 'manager-tickets' : 'worker-tickets';
    }

    logout(){
        this.authService.logout()
    }
}