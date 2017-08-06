import { PageNotFound } from './core/components/page-not-found';
import { NgModule } from '@angular/core';
import { RouterModule, Routes }  from '@angular/router';

const routes: Routes = [
  { path: '',   redirectTo: 'auth', pathMatch: 'full' },
  { path: '**', component: PageNotFound }
];
 
@NgModule({
  imports: [
    RouterModule.forRoot(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule {}