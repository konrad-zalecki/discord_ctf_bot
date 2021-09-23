# This file contains content of all messages that are sent by the bot
# on public channels, including some logic behind messages
# that contain serial data.

from leaderboard_command import get_leaderboard
from events_command import get_events


async def send_public_message(channel, message_type, context=None):
    await channel.send(render_message_content(message_type, context))


def render_message_content(message_type, context):
    if message_type in PUBLIC_MESSAGES_CONTENTS:
        return PUBLIC_MESSAGES_CONTENTS[message_type](context)
    raise Exception(f'Unknown message type: "{message_type}"')


# functions generating messages contents


def msg_non_admin_subscription_attempt(context):
    return 'Only server admin can subscribe events!'


# CONTEXT: event_name
def msg_no_such_event(context):
    return f'Sorry, there is no event named {context["event_name"]}'


# CONTEXT: event_name
def msg_channel_subscribed_event(context):
    return f'Event {context["event_name"]} is now subscribed on this channel!'


def msg_event_already_subscribed_on_channel(context):
    return 'This channel has already subscribed this event!'


def msg_event_does_not_exist(context):
    return 'Sorry, there is no such event.'


# CONTEXT: user_id
def msg_event_already_subscribed_by_user(context):
    return f'Sorry <@{context["user_id"]}>, you already subscribe this event.'


# CONTEXT: level_number, total_event_levels, user_id, event_name
def msg_broadcast_level_solved(context):
    level = context["level_number"]
    user_id = context["user_id"]
    event_levels = context["total_event_levels"]
    event_name = context["event_name"]
    broadcast_message = ''
    broadcast_message += f'<@{user_id}> has solved level {level} of event "{event_name}" '
    if level < event_levels:
        broadcast_message += f'and unlocked level {level + 1}!'
    else:
        broadcast_message += 'and finished the entire event! Congratulations!'


# CONTEXT: solver_id, event_name
def msg_broadcast_event_winner(context):
    message = ''
    message += f'<@{context["solver_id"]}> is the first participant to solve all problems'
    message += f' and therefore the winner of event "{context["event_name"]}"! Congratulations!'
    return message


# CONTEXT: help_command_with_prefix
def msg_unknown_command(context):
    return f'Unknown command. Use {context["help_command_with_prefix"]} to see available commands.'


def msg_help_command(context):
    bot_command_prefix = context["bot_command_prefix"]
    message = """===== AVAILABLE COMMANDS =====

{0}channel-subscribe-event [event_name] - subscribe event of given name to the channel command was used. After subscription, every action related to the subscribed event will be announced on that channel.
NOTE: Only server admin can subscribe event to the channel. Multiple channels may subscribe to the same event, and every message will be sent to all of these channels (even when they are on different servers).

{0}subscribe-event [event_name] - whoever uses this command will subscribe event of given name, which means they will receive event problems and will be able to send their solutions via DMs.
NOTE: Event may be subscribed by users only on text channels they were also subscribed to.

{0}leaderboard [event_name] - shows all users that subscribed event of given name with number of levels they solved.

{0}events - shows all available events.
""".format(bot_command_prefix)
    return message

# CONTEXT: command_name_with_prefix
def msg_wrong_number_of_args(context):
    return f'Invalid number of arguments. Usage: {context["command_name_with_prefix"]} [event_name]'


def msg_event_not_registered_on_channel(context):
    return 'Sorry, this event must be subscribed to this channel in order to allow users to subsribe it.'


# CONTEXT: user_id, event_name
def msg_user_registration_success(context):
    return f'<@{context["user_id"]}> subscribed event {context["event_name"]}!'


def msg_user_already_registered_to_event(context):
    return 'Sorry, you have already subscribed this event.'

# CONTEXT: event_id
def msg_leaderboard(context):
    return get_leaderboard(context["event_id"])


def msg_events(context):
    return get_events(context["channel_id"])


PUBLIC_MESSAGES_CONTENTS = {
    'NON_ADMIN_SUBSCRIPTION_ATTEMPT': msg_non_admin_subscription_attempt,
    'NO_SUCH_EVENT': msg_no_such_event,
    'CHANNEL_SUBSCRIBED_EVENT': msg_channel_subscribed_event,
    'EVENT_ALREADY_SUBSCRIBED_ON_CHANNEL': msg_event_already_subscribed_on_channel,
    'EVENT_DOES_NOT_EXIST': msg_event_does_not_exist,
    'EVENT_ALREADY_SUBSCRIBED_BY_USER': msg_event_already_subscribed_by_user,
    'BROADCAST_LEVEL_SOLVED': msg_broadcast_level_solved,
    'BROADCAST_LEVEL_WINNER': msg_broadcast_event_winner,
    'UNKNOWN_COMMAND': msg_unknown_command,
    'HELP_COMMAND': msg_help_command,
    'CHANNEL_SUBSCRIPTION_WRONG_NUMBER_OF_ARGS': msg_wrong_number_of_args,
    'USER_SUBSCRIPTION_WRONG_NUMBER_OF_ARGS': msg_wrong_number_of_args,
    'EVENT_NOT_REGISTERED_ON_CHANNEL': msg_event_not_registered_on_channel,
    'USER_EVENT_REGISTRATION_SUCCESS': msg_user_registration_success,
    'USER_ALREADY_REGISTERED_TO_EVENT': msg_user_already_registered_to_event,
    'LEADERBOARD': msg_leaderboard,
    'EVENTS': msg_events,
}