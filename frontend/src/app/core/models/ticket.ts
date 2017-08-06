export class Ticket{
    constructor(
        public ticketId: number,
        public ticketName: string,
        public creatorId: number,
        public creatorName: string,
        public creatorAvatar: string,
        public assigneeId: number,
        public assigneeName: string,
        public assigneeAvatar: string,
        public status: string,
        public created: string,
        public started: string,
        public completed: string,
        public verified: string,
    ){}

    labelClass():string{
        switch(this.status) {
            case "verified": {
                return "label-success"
            }
            case "completed": {
                return "label-info"
            }
            case "started": {
                return "label-warning"
            }
            case "assigned": {
                return "label-primary"
            }
            case "unassigned": {
                return "label-default"
            }
            default: {
                return "label-default"
            }
        }
    }

    canSwitchAssignee():boolean{
        return this.status == "assigned" || this.status == "unassigned"
    }

    canStart():boolean{
        return this.status == "assigned"
    }

    canComplete():boolean{
        return this.status == "started"
    }

    canVerify():boolean{
        return this.status == "completed"
    }

    assign(assigneeId: number, assigneeName: string){
        this.assigneeId = assigneeId
        this.assigneeName = assigneeName
        this.status = "assigned"
    }

    unassign(){
        this.assigneeId = null
        this.assigneeName = ""
        this.status = "unassigned"
    }

    start(timestamp: string){
        this.started = timestamp
        this.status = "started"
    }

    complete(timestamp: string){
        this.completed = timestamp
        this.status = "completed"
    }

    verify(timestamp: string){
        this.verified = timestamp
        this.status = "verified"
    }

    updateName(newTicketName: string){
        this.ticketName = newTicketName
    }
}