import { ToasterService } from 'angular2-toaster';
import { AuthService } from './auth.service';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { CanActivate } from '@angular/router';

@Injectable()
export class ManagerGuard implements CanActivate {

  constructor(
    private authService: AuthService, 
    private router: Router,
    private toaster: ToasterService,
  ) {}

  canActivate() {
    return this.authService.authenticatedUser.map((user)=>{
        if(user == null){
            this.toaster.pop("error", "Only authenticated users can access this page.")
            this.router.navigate(['auth'])
            return false
        }else if(!user.isManager){
            this.toaster.pop("error", "Only managers can access this page, not workers")
            this.router.navigate(['auth'])
            return false
        }else{
          return true
        }
    })
  }
}