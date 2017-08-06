import { JwtExpiredInterceptor } from './services/jwt-refresh-interceptor';
import { WebSocketService } from './services/websockets';
import { WorkerGuard } from './services/worker-guard';
import { ManagerGuard } from './services/manager-guard';
import { AuthService } from './services/auth.service';
import { SharedModule } from './../shared/shared.module';
import { Login } from './components/login';
import { AuthRoutingModule } from './auth-routing.module';
import { NgModule } from '@angular/core';
import { Http, RequestOptions } from '@angular/http';
import { AuthHttp, AuthConfig } from 'angular2-jwt';
import { HTTP_INTERCEPTORS } from '@angular/common/http';

export function authHttpServiceFactory(http: Http, options: RequestOptions) {
  return new AuthHttp(new AuthConfig({
    headerPrefix: 'JWT',
    noJwtError: true,  // will make it continue with unauthenticated request
		globalHeaders: [{'Content-Type':'application/json'}],
	}), http, options);
}

@NgModule({
  imports: [
    SharedModule,
    AuthRoutingModule,
  ],
  declarations: [
    Login
  ],
  providers: [
    AuthService,
    WebSocketService,
    ManagerGuard,
    WorkerGuard,
    {
      provide: AuthHttp,
      useFactory: authHttpServiceFactory,
      deps: [Http, RequestOptions]
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: JwtExpiredInterceptor,
      multi: true,
  }
  ]
})
export class AuthModule { }
