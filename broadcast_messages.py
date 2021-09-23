from database_logic import get_subscribing_channels

async def broadcast_to_subscribing_channels(client, event_id, message_type, context=None):
    if message_type in BROADCAST_MESSAGES_TABLE:
        for channel_id in get_subscribing_channels(event_id):
            channel = client.get_channel(channel_id)
            await channel.send(BROADCAST_MESSAGES_TABLE[message_type](context))


def broadcast_level_solved(context):
    return f'<@{context["user_id"]}> solved level {context["level_number"] - 1} of event {context["event_name"]}!'


def broadcast_event_finished(context):
    return f'<@{context["user_id"]}> finished event "{context["event_name"]}"! Congratulations!'


def broadcast_event_winner(context):
    message = ''
    message += f'Congratulations to <@{context["user_id"]}> on winning event "{context["event_name"]}"!\n'
    message += 'They are the first participant to finish that event!'
    return message


BROADCAST_MESSAGES_TABLE = {
    'LEVEL_SOLVED': broadcast_level_solved,
    'EVENT_FINISHED': broadcast_event_finished,
    'EVENT_WINNER': broadcast_event_winner
}