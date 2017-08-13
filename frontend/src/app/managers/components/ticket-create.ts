import { ToasterService } from 'angular2-toaster';
import { TicketService } from './../../core/services/tickets.service';
import { UserService } from './../../core/services/users.service';
import { Worker } from './../../core/models/worker';
import { Component, Input, ChangeDetectorRef } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal';

@Component({
    templateUrl: './ticket-create.html'
})
export class TicketCreate{
    ticketName: string
    workers: Worker[]
    assigneeId: number = -1
    
    constructor(
        private ticketService: TicketService,
        private toaster: ToasterService,
        public modal: BsModalRef,
        private cd: ChangeDetectorRef
    ){}

    setWorkers(workers: Worker[]){
        this.workers = workers
        /*
        https://github.com/valor-software/ngx-bootstrap/issues/2275
        data binding not working inside ngx-bootstrap modal
        need to manually trigger change detector
        */
        this.cd.detectChanges()
    }

    save(){
        let userId = this.assigneeId == -1 ? null : this.assigneeId
        this.ticketService.createTicket(this.ticketName, userId).subscribe(
            data => this.modal.hide(),
            error => this.toaster.pop("error", error.message)
        )
    }
}