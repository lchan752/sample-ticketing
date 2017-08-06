import { WorkersModule } from './workers/workers.module';
import { ManagersModule } from './managers/managers.module';
import { AuthModule } from './auth/auth.module';
import { CoreModule } from './core/core.module';
import { AppRoutingModule } from './app-routing.module';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { BsDropdownModule, ModalModule } from 'ngx-bootstrap';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToasterModule } from 'angular2-toaster';
import { MomentModule } from 'angular2-moment';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    ToasterModule,
    BsDropdownModule.forRoot(),
    ModalModule.forRoot(),
    MomentModule,
    HttpModule,
    CoreModule,
    AuthModule,
    ManagersModule,
    WorkersModule,
    AppRoutingModule,
  ],
  bootstrap: [AppComponent],
})
export class AppModule { }
