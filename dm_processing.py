from broadcast_messages import broadcast_to_subscribing_channels
from database_logic import *
from private_messages import send_private_message


async def handle_direct_message(client, message):
    args = message.content.upper().split()
    for dm_command in DM_COMMANDS_TABLE:
        if args[0] == dm_command:
            await DM_COMMANDS_TABLE[dm_command](client, message, args[1:], dm_command)


def validate_number_of_arguments(args, expected_args):
    return len(args) == expected_args


async def validate_event_for_dm_request(message, event_id):
    if event_id is None:
        await send_private_message(message.author, 'NON_EXISTING_EVENT')
        return False
    if not is_user_registered(message.author, event_id):
        await send_private_message(message.author, 'NOT_REGISTERED_TO_EVENT')
        return False
    if did_finish_event(message.author.id, event_id):
        await send_private_message(message.author, 'EVENT_ALREADY_FINISHED')
        return False
    return True


async def dm_solve(client, message, args, command_name):
    EXPECTED_SOLVE_ARGS = 2
    if not validate_number_of_arguments(args, EXPECTED_SOLVE_ARGS):
        return await send_private_message(message.author, 'SOLVE_USAGE', {"command_name": command_name})
    event_name = args[0].lower()
    flag = args[1]
    event_id = get_event_id(event_name)
    if not await validate_event_for_dm_request(message, event_id):
        return
    if is_correct_solution(message.author.id, event_id, flag):
        await send_private_message(message.author, 'CORRECT_FLAG')
        level_up(message.author.id, event_id)
        broadcast_context = {
            "event_name": event_name,
            "user_id": message.author.id,
            "level_number": get_user_current_level_in_event(message.author.id, event_id),
        }
        await broadcast_to_subscribing_channels(client, event_id, 'LEVEL_SOLVED', broadcast_context)
        if did_finish_event(message.author.id, event_id):
            await send_private_message(message.author, 'EVENT_COMPLETED', {'event_name': event_name})
            if how_many_completions(event_id) == 1:
                await broadcast_to_subscribing_channels(client, event_id, 'EVENT_WINNER', broadcast_context)
            else:
                await broadcast_to_subscribing_channels(client, event_id, 'EVENT_FINISHED', broadcast_context)
        else:
            new_level = get_user_current_level_in_event(message.author.id, event_id)
            context = {"event_id": event_id, "level_number": new_level}
            await send_private_message(message.author, 'NEW_LEVEL_UNLOCKED', context)
    else:
        return await send_private_message(message.author, 'WRONG_FLAG')


async def dm_resend(client, message, args, command_name):
    EXPECTED_RESEND_ARGS = 1
    if not validate_number_of_arguments(args, EXPECTED_RESEND_ARGS):
        return await send_private_message(message.author, 'RESEND_USAGE', {"command_name": command_name})
    event_name = args[0].lower()
    event_id = get_event_id(event_name)
    if not await validate_event_for_dm_request(message, event_id):
        return
    resend_context = {
        "event_id": event_id,
        "level_number": get_user_current_level_in_event(message.author.id, event_id),
        "event_name": event_name,
    }
    await send_private_message(message.author, 'RESEND_LEVEL', resend_context)


async def dm_subs(client, message, args, command_name):
    EXPECTED_SUBS_ARGS = 0
    if not validate_number_of_arguments(args, EXPECTED_SUBS_ARGS):
        return await send_private_message(message.author, 'NO_ARGS_NEEDED', {"command_name": command_name})
    await send_private_message(message.author, 'SUBS', {"user_id": message.author.id})


async def dm_help(client, message, args, command_name):
    EXPECTED_HELP_ARGS = 0
    if not validate_number_of_arguments(args, EXPECTED_HELP_ARGS):
        return await send_private_message(message.author, 'NO_ARGS_NEEDED', {"command_name": command_name})
    await send_private_message(message.author, 'HELP')


DM_COMMANDS_TABLE = {
    'SOLVE': dm_solve,
    'RESEND': dm_resend,
    'SUBS': dm_subs,
    'HELP': dm_help,
}