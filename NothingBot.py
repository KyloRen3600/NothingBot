try:
	from .Addon import *
except:
	from Addon import *
from NothingAPI.core import log
import discord
from discord.ext import commands


log("INFO", "NothingBot Version 1.0.0")
log("INFO", "Developed by NothingGames")
log("INFO", "Starting...\n ")

TOKEN = "METTRE LE TOKEN ICI"
prefix = "!"
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")
core = Addon(bot, "core/core.json")
core.import_script()

log("INFO", "Loading Addons...")
load_addons(bot)


log("INFO", "Logging to Bot...\n ")
bot.run(TOKEN)