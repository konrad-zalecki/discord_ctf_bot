from public_messages import send_public_message
from private_messages import send_private_message
from database_logic import *

BOT_COMMAND_PREFIX = '--'
HELP_COMMAND = 'HELP'

async def handle_public_message(message):
    if is_command(message.content):
        await process_command(message)


def is_command(message_content):
    return message_content.startswith(BOT_COMMAND_PREFIX)


async def process_command(message):
    for command in COMMANDS_AND_HANDLERS:
        if message.content.upper().startswith((BOT_COMMAND_PREFIX + command).upper()):
            return await COMMANDS_AND_HANDLERS[command](message, command)
    context = {"help_command_with_prefix": BOT_COMMAND_PREFIX + HELP_COMMAND.lower()}
    await send_public_message(message.channel, 'UNKNOWN_COMMAND', context)


async def handle_help_command(client, message, command_name):
    await send_public_message(message.channel, 'HELP_COMMAND', {"bot_command_prefix": BOT_COMMAND_PREFIX})


def is_server_admin(message_author):
    return message_author.guild_permissions.administrator


# use only when 'message_content' is a valid bot command
def get_command_arguments(message_content):
    return message_content.upper().split()[1:]


async def handle_channel_subscription_command(message, command_name):
    EXPECTED_NUMBER_OF_ARGUMENTS_IN_CHANNEL_SUBSCRIPTION = 1
    if not is_server_admin(message.author):
        return await send_public_message(message.channel, 'NON_ADMIN_SUBSCRIPTION_ATTEMPT')
    args = get_command_arguments(message.content)
    if len(args) != EXPECTED_NUMBER_OF_ARGUMENTS_IN_CHANNEL_SUBSCRIPTION:
        context = {'command_name_with_prefix': BOT_COMMAND_PREFIX +  command_name.lower()}
        return await send_public_message(message.channel, 'CHANNEL_SUBSCRIPTION_WRONG_NUMBER_OF_ARGS', context)
    event_name = args[0].lower()
    event_id = get_event_id(event_name)
    if event_id is None:
        return await send_public_message(message.channel, 'EVENT_DOES_NOT_EXIST')
    if register_channel(message.channel, event_id):
        return await send_public_message(message.channel, 'CHANNEL_SUBSCRIBED_EVENT', {"event_name": event_name})
    else:
        return await send_public_message(message.channel, 'EVENT_ALREADY_SUBSCRIBED_ON_CHANNEL')


async def handle_user_subscription_command(message, command_name):
    EXPECTED_NUMBER_OF_ARGUMENTS_IN_USER_SUBSCRIPTION = 1
    args = get_command_arguments(message.content)
    if len(args) != EXPECTED_NUMBER_OF_ARGUMENTS_IN_USER_SUBSCRIPTION:
        context = {'command_name_with_prefix': BOT_COMMAND_PREFIX + command_name.lower()}
        return await send_public_message(message.channel, 'USER_SUBSCRIPTION_WRONG_NUMBER_OF_ARGS', context)
    event_name = args[0].lower()
    event_id = get_event_id(event_name)
    if event_id is None:
        return await send_public_message(message.channel, 'EVENT_DOES_NOT_EXIST')
    if not is_channel_registered(message.channel, event_id):
        context = {"event_name": event_name}
        return await send_public_message(message.channel, 'EVENT_NOT_REGISTERED_ON_CHANNEL', context)
    if register_user(message.author, event_id):
        context = {"user_id": message.author.id, "event_name": event_name, "event_id": event_id}
        await send_public_message(message.channel, 'USER_EVENT_REGISTRATION_SUCCESS', context)
        await send_private_message(message.author, 'EVENT_SUBSCRIBED', context)
        return
    else:
        return await send_public_message(message.channel, 'USER_ALREADY_REGISTERED_TO_EVENT')


async def handle_leaderboard_command(message, command_name):
    EXPECTED_NUMBER_OF_ARGUMENTS = 1
    args = get_command_arguments(message.content)
    if len(args) != EXPECTED_NUMBER_OF_ARGUMENTS:
        context = {'command_name_with_prefix': BOT_COMMAND_PREFIX + command_name.lower()}
        return await send_public_message(message.channel, 'USER_SUBSCRIPTION_WRONG_NUMBER_OF_ARGS', context)
    event_name = args[0].lower()
    event_id = get_event_id(event_name)
    if event_id is None:
        return await send_public_message(message.channel, 'EVENT_DOES_NOT_EXIST')
    if not is_channel_registered(message.channel, event_id):
        context = {"event_name": event_name}
        return await send_public_message(message.channel, 'EVENT_NOT_REGISTERED_ON_CHANNEL', context)
    await send_public_message(message.channel, 'LEADERBOARD', {"event_id": event_id})


async def handle_events_command(message, command_name):
    EXPECTED_NUMBER_OF_ARGUMENTS = 0
    args = get_command_arguments(message.content)
    if len(args) != EXPECTED_NUMBER_OF_ARGUMENTS:
        context = {'command_name_with_prefix': BOT_COMMAND_PREFIX + command_name.lower()}
        return await send_public_message(message.channel, 'USER_SUBSCRIPTION_WRONG_NUMBER_OF_ARGS', context)
    await send_public_message(message.channel, 'EVENTS', {"channel_id": message.channel.id})


COMMANDS_AND_HANDLERS = {
    HELP_COMMAND: handle_help_command,
    'CHANNEL-SUBSCRIBE-EVENT': handle_channel_subscription_command,
    'SUBSCRIBE-EVENT': handle_user_subscription_command,
    'LEADERBOARD': handle_leaderboard_command,
    'EVENTS': handle_events_command,
}