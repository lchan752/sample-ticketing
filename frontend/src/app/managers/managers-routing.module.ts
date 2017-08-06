import { ManagerGuard } from './../auth/services/manager-guard';
import { ManagerTicketList } from './components/manager-ticket-list';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router'

const routes: Routes = [
  { path: 'manager-tickets', component: ManagerTicketList, canActivate: [ManagerGuard] },
];
 
@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class ManagersRoutingModule {}