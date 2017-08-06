import { environment } from './../../../environments/environment';
import { Worker } from './../models/worker';
import { Observable } from 'rxjs/Observable';
import { AuthHttp } from 'angular2-jwt';
import { Injectable } from '@angular/core';
@Injectable()
export class UserService{
    constructor(private authHttp: AuthHttp){}

    getWorkers():Observable<Worker[]>{
        return this.authHttp.get(environment.api_root + '/users/workers/').map(
            response => {
                let workers: Worker[] = []
                for(let data of response.json()){
                    let worker = new Worker(
                        data.user_id,
                        data.full_name,
                    )
                    workers.push(worker)
                }
                return workers
            }
        )
    }
}