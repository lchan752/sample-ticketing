import { WorkerGuard } from './../auth/services/worker-guard';
import { WorkerTicketList } from './components/worker-ticket-list';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router'

const routes: Routes = [
  { path: 'worker-tickets', component: WorkerTicketList, canActivate: [WorkerGuard] },
];
 
@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class WorkersRoutingModule {}