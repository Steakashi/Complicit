from entities import Room, User, Game


def _generate_message(action, client_id, **args):
        message = dict()
        for key, value in args.items():
            if type(value) == list:
                message[key] = [single_value.flattened for single_value in value]
            elif type(value) in [Room, User, Game]:
                message[key] = value.flattened
            else:
                message[key] = value

        message.update(
            {
                'action': action,
                'client_id': client_id,
            }
        )

        return message


def error(client_id, error):
    return _generate_message(
        action="error", 
        client_id=client_id, 
        error=error
    )


def success(client_id, success):
    return _generate_message(
        action="success", 
        client_id=client_id, 
        success=success
    )


def default(action, client_id, **args):
    return _generate_message(action, client_id, **args)  