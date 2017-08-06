import { ToasterService } from 'angular2-toaster';
import { WebSocketService } from './../../auth/services/websockets';
import { TicketService } from './../../core/services/tickets.service';
import { Ticket } from './../../core/models/ticket';
import { Component, Input, OnInit } from '@angular/core';

@Component({
    selector: 'div[worker-ticket]',
    templateUrl: './worker-ticket.html',
    styleUrls: ['./worker-ticket.css'],
})
export class WorkerTicket implements OnInit{
    @Input('ticket') ticket: Ticket
    
    constructor(
        private ticketService: TicketService, 
        private toaster: ToasterService,
        private ws: WebSocketService
    ){}

    ngOnInit(){
        this.ws.getDataStream().subscribe((msg)=>{
            this.handleEvent(JSON.parse(msg.data))
        })
    }

    startTicket(){
        this.ticketService.startTicket(this.ticket.ticketId).subscribe(
            data => data,
            error => this.toaster.pop("error", error.message)
        )
    }

    completeTicket(){
        this.ticketService.completeTicket(this.ticket.ticketId).subscribe(
            data => data,
            error => this.toaster.pop("error", error.message)
        )
    }

    hasTicketActions():boolean{
        return this.ticket.canStart() || this.ticket.canComplete()
    }

    handleEvent(data: any){
        if(data.ticket.id != this.ticket.ticketId){
            return
        }

        switch(data.event){
            case 'updated':{
                this.ticket.updateName(data.ticket.name)
                this.toaster.pop('info', 'Ticket Updated by ' + this.ticket.creatorName)
                break
            }
            case 'started':{
                this.ticket.start(data.ticket.started)
                this.toaster.pop('success', 'Ticket Started')
                break
            }
            case 'completed':{
                this.ticket.complete(data.ticket.completed)
                this.toaster.pop('success', 'Ticket Completed')
                break
            }
            case 'verified':{
                this.ticket.verify(data.ticket.verified)
                this.toaster.pop("info", "Ticket Verified by " + this.ticket.creatorName)
                break
            }
            default:{
                break
            }
        }
    }
}