import { Observable } from 'rxjs/Observable';
import { AuthenticatedUser } from './../models/auth-user';
import { environment } from './../../../environments/environment';
import { AuthService } from './auth.service';
import { $WebSocket } from 'angular2-websocket/angular2-websocket';
import { Injectable } from '@angular/core'

@Injectable()
export class WebSocketService{
    private ws: $WebSocket

    constructor(private authService: AuthService){
        this.authService.authenticatedUser.subscribe((user)=>{
            if(user != null){
                this.connect(user)
            }else{
                this.disconnect()
            }
        })
    }

    getDataStream():Observable<any>{
        return this.ws.getDataStream()
    }

    isConnected():boolean{
        return this.ws != null && this.ws.getReadyState() in [0, 1]
    }

    connect(user: AuthenticatedUser){
        if(this.isConnected()){
            this.disconnect()
        }
        let token = this.authService.getToken()
        this.ws = new $WebSocket(environment.websocket_root + "/users/"+user.userId+"/?token="+token);
        // this.ws.onMessage((msg: MessageEvent)=>{
        //     console.log("websockets: ", msg.data)
        // })
    }

    disconnect(){
        this.ws.close()
    }
}