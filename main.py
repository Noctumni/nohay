import discord
from discord.ext import commands
import os

# Importing modules
import economy
import pets
import hunt
import shop
import inventory
import cooldowns
import xp
import utils

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="owo ", intents=intents)

# Load data once
economy.load_data()
pets.load_data()
hunt.load_data()
shop.load_data()
inventory.load_data()
cooldowns.load_data()
xp.load_data()
utils.load_data()

# Register commands from modules
economy.register_commands(bot)
pets.register_commands(bot)
hunt.register_commands(bot)
shop.register_commands(bot)
inventory.register_commands(bot)
xp.register_commands(bot)
utils.register_commands(bot)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

bot.run(os.environ['DISCORD_TOKEN'])
