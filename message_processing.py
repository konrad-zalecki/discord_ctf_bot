import discord
from commands_processing import handle_public_message
from dm_processing import handle_direct_message


def is_direct_message_channel(channel):
    return isinstance(channel, discord.channel.DMChannel)


async def handle_message(client, message):
    if message.author == client.user:
        return # bot should ignore messages sent by itself
    if is_direct_message_channel(message.channel):
        await handle_direct_message(client, message)
    else:
        await handle_public_message(message)