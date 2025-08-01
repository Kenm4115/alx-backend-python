def get_threaded_messages(message):
    """ Recursively get replies for a message. """
    thread = {
        'message': message,
        'replies': [get_threaded_messages(reply) for reply in message.replies.all().order_by('timestamp')]
    }
    return thread
