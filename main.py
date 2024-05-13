import discord, serverping, os, json, requests, time, asyncio
from discord.ext import commands

TOKEN = 'MTIzOTAzNTY0NzEyNjE0Mjk4Nw.GbaGS-.8GqToBDtds8cqsU-CdLAN8VrvGLb2JRvYCDKtg'
SERVER_ID = '1239035503450263642'
ONLINE_PLAYERS_CHANNEL_ID = '1239037034560225422'
ONLINE_PLAYERS_MESSAGE_ID = '1239039873839796224'
TRACK_PLAYERS_CHANNEL_ID = '1239043499190652980'

intents = discord.Intents.default()
intents.message_content = True

players_after = []
players_before = serverping.get_players_from_server()

bot = commands.Bot(command_prefix='?', intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    while True:
        players = serverping.get_players_from_server()
        await track_online_players()
        await update_players(players)
        await status_bar_presence_wait(5)

async def send_message_to_discord(message, channel):
    channel = bot.get_channel(int(channel))
    await channel.send(message)

async def status_bar_presence_wait(time):
    while time > 0:
        await bot.change_presence(activity=discord.Game(name=f"Refresh in: {time}s"))
        await asyncio.sleep(2)
        time -= 2
    await bot.change_presence(activity=discord.Game(name="Updating..."))

async def update_players(players):
    channel = bot.get_channel(int(ONLINE_PLAYERS_CHANNEL_ID))
    message = await channel.fetch_message(ONLINE_PLAYERS_MESSAGE_ID)
    await message.edit(content=f"Players online: {players}")

async def track_online_players():
    global players_before
    players_after = serverping.get_players_from_server()
    new_players = list(set(players_after) - set(players_before))
    left_players = list(set(players_before) - set(players_after))
    if new_players:
        for player in new_players:
            await send_message_to_discord(f"{player} has joined the server", TRACK_PLAYERS_CHANNEL_ID)
    if left_players:
        for player in left_players:
            await send_message_to_discord(f"{player} has left the server", TRACK_PLAYERS_CHANNEL_ID)
    players_before = players_after

bot.run(TOKEN)
