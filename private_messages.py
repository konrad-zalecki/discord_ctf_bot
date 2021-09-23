import discord
from database_logic import get_event_name, get_problem_name
from user_subs import get_user_subs_message


def create_attachment(event_id, level_number):
    event_name = get_event_name(event_id)
    file_name = event_name + f", level {level_number}, " + get_problem_name(event_id, level_number) + ".zip"
    return discord.File(f'events\\{event_name}\\{level_number}\\{level_number}.zip', filename=file_name)


async def send_private_message(user, message_type, context=None):
    if message_type in PRIVATE_MESSAGES_TABLE:
        message_content, attachment = PRIVATE_MESSAGES_TABLE[message_type](context)
        if attachment is None:
            await user.send(message_content)
        else:
            await user.send(message_content, file=attachment)
        return
    else:
        raise Exception(f'Unknown dm message type: "{message_type}"')


def dm_event_subscribed(context):
    message = ''
    message += f'Hi! You receive this message, because you\'ve just subscribed to event "{context["event_name"]}".\n'
    message += 'Here is first problem from this event!\n'
    message += 'If you want to know how to send problem solution, send "help" message to me!'
    return (message, create_attachment(context["event_id"], 1))


def dm_solve_usage(context):
    message = ''
    message += f'Invalid number of arguments. Usage: {context["command_name"]} [event_name] [solution_flag]\n'
    message += 'NOTE: flag name should not contain any whitespace!'
    return (message, None)


def dm_non_existing_event(context):
    return ('Sorry, there is no such event.', None)


def dm_not_registered_to_event(context):
    return ('Sorry, you are not registered to this event.', None)


def dm_event_already_finished(context):
    return ('You already finished this event, nothing to solve!', None)


def dm_correct_flag(context):
    return ('Correct!', None)


def dm_wrong_flag(context):
    return ('Wrong answer. Try again!', None)


def dm_new_level_unlocked(context):
    event_id = context["event_id"]
    level_number = context["level_number"]
    event_name = get_event_name(event_id)
    message = f'You unlocked level {level_number} of event "{event_name}"!'
    return (message, create_attachment(event_id, level_number))


def dm_event_completed(context):
    return (f'You finished event {context["event_name"]}! Congratulations!', None)


def dm_resend_usage(context):
    return (f'Invalid number of arguments. Usage: {context["command_name"]} [event_name]\n', None)


def dm_resend_level(context):
    file_to_send = create_attachment(context["event_id"], context["level_number"])
    return (f'Resending latest unlocked level for event "{context["event_name"]}"', file_to_send)


def dm_subs(context):
    return (get_user_subs_message(context["user_id"]), None)


def dm_no_args_needed(context):
    return (f'No arguments are accepted for command "{context["command_name"]}"\n.')


def dm_help(context):
    DM_HELP_MESSAGE = """Commands available in direct messages:

solve [event_name] [problem_flag] - submits a solution to your newest unsolved problem from event of given name.
For example, if you want to submit solution to a problem in event named COOL_EVENT, then you should send message:
solve COOL_EVENT VERY_COOL_FLAG
NOTE: it's not required to provide number of level you want to solve - it's always the latest level you unlocked and hasn't solved yet.

resend [event_name] - resends files associated with your newest unsolved problem from event of given name (the problem that you currently have to solve)

subs - lists all events that you have subscribed

NOTE: In direct messages, there is no prefix used in all commands."""
    return (DM_HELP_MESSAGE, None)


PRIVATE_MESSAGES_TABLE = {
    'EVENT_SUBSCRIBED': dm_event_subscribed,
    'INVALID_NUMBER_OF_ARGUMENTS': dm_solve_usage,
    'NON_EXISTING_EVENT': dm_non_existing_event,
    'NOT_REGISTERED_TO_EVENT': dm_not_registered_to_event,
    'EVENT_ALREADY_FINISHED': dm_event_already_finished,
    'CORRECT_FLAG': dm_correct_flag,
    'WRONG_FLAG': dm_wrong_flag,
    'NEW_LEVEL_UNLOCKED': dm_new_level_unlocked,
    'EVENT_COMPLETED': dm_event_completed,
    'RESEND_USAGE': dm_resend_usage,
    'RESEND_LEVEL': dm_resend_level,
    'SUBS': dm_subs,
    'NO_ARGS_NEEDED': dm_no_args_needed,
    'HELP': dm_help,
}