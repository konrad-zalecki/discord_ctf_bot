from database_logic import get_all_events_subscribed_for_user, get_event_name, get_user_current_level_in_event, get_event_levels


def get_user_subs_message(user_id):
    user_subs = get_all_events_subscribed_for_user(user_id)
    message = 'Events you have subscribed:\n'
    for event_id in user_subs:
        message += '- ' + get_event_name(event_id)
        message += f' ({get_user_current_level_in_event(user_id, event_id) - 1}/{get_event_levels(event_id)})\n'
    return message