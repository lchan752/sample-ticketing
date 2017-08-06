import { ToasterService } from 'angular2-toaster';
import { WebSocketService } from './../../auth/services/websockets';
import { Worker } from './../../core/models/worker';
import { TicketService } from './../../core/services/tickets.service';
import { Ticket } from './../../core/models/ticket';
import { Component, Input, OnChanges, SimpleChanges, OnInit } from '@angular/core';

@Component({
    selector: 'div[manager-ticket]',
    templateUrl: './manager-ticket.html',
    styleUrls: ['./manager-ticket.css'],
})
export class ManagerTicket implements OnChanges, OnInit{
    @Input('ticket') ticket: Ticket
    @Input('workers') workers: Worker[]
    selectedWorkerId: number
    updatedTicketName: string
    isUpdatingTicketName: boolean = false
    
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

    ngOnChanges(changes: SimpleChanges){
        if(this.ticket){
            this.selectedWorkerId = this.ticket.assigneeId == null ? -1 : this.ticket.assigneeId
            this.updatedTicketName = this.ticket.ticketName
        }
    }

    toggleEditMode(){
        this.isUpdatingTicketName = !this.isUpdatingTicketName
    }

    hasTicketActions(){
        return this.ticket.canVerify()
    }
    
    assignTicket(){
        if(this.selectedWorkerId == -1){
            this.ticketService.unassignTicket(this.ticket.ticketId).subscribe(
                data => data,
                error => this.toaster.pop("error", error.message)
            )
        }else{
            this.ticketService.assignTicket(this.ticket.ticketId, this.selectedWorkerId).subscribe(
                data => data,
                error => this.toaster.pop("error", error.message)
            )
        }
    }

    verifyTicket(){
        this.ticketService.verifyTicket(this.ticket.ticketId).subscribe(
            data => data,
            error => this.toaster.pop("error", error.message)
        )
    }

    updateTicketName(){
        this.ticketService.updateTicketName(this.ticket.ticketId, this.updatedTicketName).subscribe(
            data => data,
            error => this.toaster.pop("error", error.message)
        )
        this.toggleEditMode()
    }

    handleEvent(data: any){
        if(data.ticket.id != this.ticket.ticketId){
            return
        }
        
        switch(data.event){
            case 'updated':{
                this.ticket.updateName(data.ticket.name)
                this.toaster.pop('success', 'Ticket Updated')
                break
            }
            case 'assigned':{
                this.ticket.assign(data.ticket.assignee.id, data.ticket.assignee.full_name)
                this.toaster.pop('success', 'Ticket Assigned to ' + this.ticket.assigneeName)
                break
            }
            case 'unassigned':{
                this.ticket.unassign()
                this.toaster.pop('success', 'Ticket Unassigned')
                break
            }
            case 'started':{
                this.ticket.start(data.ticket.started)
                this.toaster.pop('info', 'Ticket Started By ' + this.ticket.assigneeName)
                break
            }
            case 'completed':{
                this.ticket.complete(data.ticket.completed)
                this.toaster.pop('info', 'Ticket Completed By ' + this.ticket.assigneeName)
                break
            }
            case 'verified':{
                this.ticket.verify(data.ticket.verified)
                this.toaster.pop("success", "Ticket Verified")
                break
            }
            default:{
                break
            }
        }
    }
}