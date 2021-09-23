from database_logic import get_all_events, get_registered_events, get_event_name, get_event_levels


def get_events(channel_id):
    all_events = get_all_events()
    registered_events = get_registered_events(channel_id)
    message_to_send = 'All available events:\n'
    for level_id in all_events:
        star = '*' if level_id in registered_events else ''
        message_to_send += f'- {get_event_name(level_id)} ({get_event_levels(level_id)} levels){star}\n'
    message_to_send += '\nNOTE: events marked with "*" are already subscribed to this channel'
    return message_to_send