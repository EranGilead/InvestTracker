import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

# Create a new bot instanceintents = discord.Intents.default()
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Event to indicate the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Command to make the bot say hello
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

# Run the bot with the token
bot.run(TOKEN)