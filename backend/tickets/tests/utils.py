def expected_data(ticket):
    data = {
        'ticket_id': ticket.id,
        'ticket_name': ticket.name,
        'creator_id': ticket.creator.id,
        'creator_fullname': ticket.creator.get_full_name(),
        'creator_avatar': ticket.creator.avatar,
        'assignee_id': ticket.assignee.id if ticket.assignee else None,
        'assignee_fullname': ticket.assignee.get_full_name() if ticket.assignee else '',
        'assignee_avatar': ticket.assignee.avatar if ticket.assignee else None,
        'status': ticket.status(),
        'created': ticket.created,
        'started': ticket.started,
        'completed': ticket.completed,
        'verified': ticket.verified
    }
    return data