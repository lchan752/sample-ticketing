
import { WorkersRoutingModule } from './workers-routing.module';
import { WorkerTicketList } from './components/worker-ticket-list';
import { WorkerTicket } from './components/worker-ticket';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

@NgModule({
  imports: [
    CommonModule,
    WorkersRoutingModule,
  ],
  declarations: [
    WorkerTicketList,
    WorkerTicket,
  ]
})
export class WorkersModule { }
