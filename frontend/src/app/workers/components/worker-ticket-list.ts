import { ToasterService } from 'angular2-toaster';
import { WebSocketService } from './../../auth/services/websockets';
import { TicketService } from './../../core/services/tickets.service';
import { Ticket } from './../../core/models/ticket';
import { Router } from '@angular/router';
import { AuthService } from './../../auth/services/auth.service';
import { Component, OnInit } from '@angular/core';
@Component({
    templateUrl: './worker-ticket-list.html'
})
export class WorkerTicketList implements OnInit{
    tickets: Ticket[]
    
    constructor(
        private authService: AuthService,
        private ticketService: TicketService,
        private ws: WebSocketService,
        private toaster: ToasterService,
        private router: Router,
    ){}

    ngOnInit(){
        this.authService.authenticatedUser.subscribe((user)=>{
            if(user == null || user.isManager){
                this.router.navigate(['auth'])
            }else{
                this.getTickets()
            }
        })

        this.ws.getDataStream().subscribe((msg)=>{
            this.handleEvent(JSON.parse(msg.data))
        })
    }

    getTickets(){
        this.ticketService.getTickets().subscribe(
            tickets => {
                this.tickets = tickets
            }
        )
    }

    handleEvent(data: any){
        switch(data.event){
            case 'assigned':{
                this.getTickets()
                this.toaster.pop("info", "A new ticket is assigned to you")
                break
            }
            case 'unassigned':{
                this.getTickets()
                this.toaster.pop("info", "A ticket is unassigned from you")
                break
            }
            case 'reassigned':{
                this.getTickets()
                this.toaster.pop("info", "A ticket is reassigned to " + data.ticket.assignee.full_name)
                break
            }
            case 'created':{
                this.getTickets()
                this.toaster.pop("info", "A new ticket is assigned to you")
                break
            }
            default:{
                break
            }
        }
    }
}