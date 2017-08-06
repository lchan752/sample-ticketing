import { ToasterService } from 'angular2-toaster';
import { Observable } from 'rxjs/Observable';
import { Ticket } from './../../core/models/ticket';
import { environment } from './../../../environments/environment';
import { AuthHttp } from 'angular2-jwt';
import { Injectable } from '@angular/core';

@Injectable()
export class TicketService{
    constructor(private authHttp: AuthHttp, private toaster: ToasterService){}

    logSuccess(resp: any): Response{
        //console.log(resp)
        return resp
    }

    logError(err: any): Observable<Response>{
        console.log(err)
        let message = JSON.parse(err._body)
        return Observable.throw(new Error(message.detail))
    }

    getTickets():Observable<Ticket[]>{
        return this.authHttp
        .get(environment.api_root + '/tickets/')
        .map(response => {
            let tickets: Ticket[] = []
            for(let data of response.json()){
                let ticket = new Ticket(
                    data.ticket_id,
                    data.ticket_name,
                    data.creator_id,
                    data.creator_fullname,
                    data.creator_avatar,
                    data.assignee_id,
                    data.assignee_fullname,
                    data.assignee_avatar,
                    data.status,
                    data.created,
                    data.started,
                    data.completed,
                    data.verified,
                )
                tickets.push(ticket)
            }
            return tickets
        })
    }

    assignTicket(ticketId: number, assigneeId: number){
        let postData = {assignee_id: assigneeId}
        return this.authHttp
        .post(environment.api_root + '/tickets/' + ticketId + '/assign/', postData)
        .map(this.logSuccess)
        .catch(this.logError)
    }

    unassignTicket(ticketId: number){
        return this.authHttp
        .post(environment.api_root + '/tickets/' + ticketId + '/unassign/', {})
        .map(this.logSuccess)
        .catch(this.logError)
    }

    verifyTicket(ticketId: number){
        return this.authHttp
        .post(environment.api_root + '/tickets/' + ticketId + '/verify/', {})
        .map(this.logSuccess)
        .catch(this.logError)
    }

    startTicket(ticketId: number){
        return this.authHttp
        .post(environment.api_root + '/tickets/' + ticketId + '/start/', {})
        .map(this.logSuccess)
        .catch(this.logError)
    }

    completeTicket(ticketId: number){
        return this.authHttp
        .post(environment.api_root + '/tickets/' + ticketId + '/complete/', {})
        .map(this.logSuccess)
        .catch(this.logError)
    }

    updateTicketName(ticketId: number, ticketName: string){
        let postData = {ticket_name: ticketName}
        return this.authHttp
        .post(environment.api_root + '/tickets/' + ticketId + '/update/', postData)
        .map(this.logSuccess)
        .catch(this.logError)
    }

    createTicket(ticketName: string, assigneeId: number){
        let postData = {name: ticketName, assignee: assigneeId,}
        return this.authHttp
        .post(environment.api_root + '/tickets/create/', postData)
        .map(this.logSuccess)
        .catch(this.logError)
    }
}