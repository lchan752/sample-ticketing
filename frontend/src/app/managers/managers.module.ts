import { TicketCreate } from './components/ticket-create';
import { ManagerTicketList } from './components/manager-ticket-list';
import { ManagerTicket } from './components/manager-ticket';
import { ManagersRoutingModule } from './managers-routing.module';
import { SharedModule } from './../shared/shared.module';
import { NgModule } from '@angular/core';

@NgModule({
  imports: [
    SharedModule,
    ManagersRoutingModule,
  ],
  declarations: [
    ManagerTicketList,
    ManagerTicket,
    TicketCreate,
  ],
  entryComponents:[
    TicketCreate,
  ]
})
export class ManagersModule { }
