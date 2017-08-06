export class AuthenticatedUser{
    constructor(
        public userId: number,
        public name: string,
        public avatar: string,
        public isManager:boolean){}
}