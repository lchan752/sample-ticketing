import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BsDropdownModule, ModalModule } from 'ngx-bootstrap';

@NgModule({
  imports: [
    CommonModule,
  ],
  declarations: [],
  exports:  [
    CommonModule,
    FormsModule,
    BsDropdownModule,
    ModalModule,
  ]
})
export class SharedModule { }
