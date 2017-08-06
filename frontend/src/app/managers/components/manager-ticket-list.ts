import { WebSocketService } from './../../auth/services/websockets';
import { TicketCreate } from './ticket-create';
import { UserService } from './../../core/services/users.service';
import { Worker } from './../../core/models/worker';
import { Subject } from 'rxjs/Rx';
import { TicketService } from './../../core/services/tickets.service';
import { Ticket } from './../../core/models/ticket';
import { Router } from '@angular/router';
import { AuthService } from './../../auth/services/auth.service';
import { Component, OnInit } from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';

@Component({
    templateUrl: './manager-ticket-list.html'
})
export class ManagerTicketList implements OnInit{
    tickets: Ticket[] = []
    workers: Worker[] = []
    
    constructor(
        private authService: AuthService,
        private ticketService: TicketService,
        private userService: UserService,
        private ws: WebSocketService,
        private modalService: BsModalService,
        private router: Router
    ){}

    ngOnInit(){
        this.authService.authenticatedUser.subscribe((user)=>{
            if(user == null || !user.isManager){
                this.router.navigate(['auth'])
            }else{
                this.getTickets()
                this.getWorkers()
            }
        })

        this.ws.getDataStream().subscribe((msg)=>{
            this.handleEvent(JSON.parse(msg.data))
        })
    }

    createTicket(){
        let modal = this.modalService.show(TicketCreate)
        let comp = <TicketCreate>modal.content
        comp.setWorkers(this.workers)
    }

    getTickets(){
        this.ticketService.getTickets().subscribe(
            tickets => {
                this.tickets = tickets
            }
        )
    }

    getWorkers(){
        this.userService.getWorkers().subscribe(
            workers => {
                this.workers = workers
            }
        )
    }

    handleEvent(data: any){
        switch(data.event){
            case 'created':{
                this.getTickets()
                break
            }
            default:{
                break
            }
        }
    }
}