import discord
from message_processing import handle_message

BOT_TOKEN = 'B0tT0k3nH3r3' # TODO: put your discord bot token here

def main():
    client = discord.Client()

    @client.event
    async def on_ready():
        print('Bot is active as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        await handle_message(client, message)

    client.run(BOT_TOKEN)


if __name__ == '__main__':
    main()