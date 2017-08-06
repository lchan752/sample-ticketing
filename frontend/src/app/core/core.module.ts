import { UserService } from './services/users.service';
import { TicketService } from './services/tickets.service';
import { AuthRoutingModule } from './../auth/auth-routing.module';
import { ManagersRoutingModule } from './../managers/managers-routing.module';
import { WorkersRoutingModule } from './../workers/workers-routing.module';
import { SharedModule } from './../shared/shared.module';
import { Navbar } from './components/navbar';
import { PageNotFound } from './components/page-not-found';
import { NgModule } from '@angular/core';

@NgModule({
  imports: [
    SharedModule,
    AuthRoutingModule,
    WorkersRoutingModule,
    ManagersRoutingModule,
  ],
  declarations: [
    PageNotFound,
    Navbar,
  ],
  exports: [
    Navbar,
  ],
  providers: [
    TicketService,
    UserService,
  ]
})
export class CoreModule { }
