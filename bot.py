import discord
import os
import sys
from discord.ext import commands
import logging
from collections import Counter
import json

h = "info.json"
if not os.path.exists(h):
    with open(h, "w") as f:
        writeJ = '{"PREFIX": "None", "TOKEN": "None", "OWNER": "None"}'
        parse = json.loads(writeJ)
        f.write(json.dumps(parse, indent=4, sort_keys=True))
        f.truncate()
else:
    print("Starting with current info.json")

with open("info.json") as f:
    config = json.load(f)


description = '''A Bot Made by Teddy And Dangerous through Discord.py.'''
bot = commands.Bot(command_prefix=config["PREFIX"], description=description, pm_help=True)

@bot.event
async def on_ready():
    users = len(set(bot.get_all_members()))
    servers = len(bot.servers)
    channels = len([c for c in bot.get_all_channels()])
    print('+-------------Deddy-------------+')
    print('Logged in as\n{}({})'.format(bot.user.name,bot.user.id))
    print('+------Current Statistics------+')
    #print('')
    print("{} servers".format(servers))
    print("{} channels".format(channels))
    print("{} users".format(users))
    print('-----------------------------')

def init_logging(bot):
    logging.root.setLevel(logging.INFO)
    logger = logging.getLogger('Logs')
    logger.setLevel(logging.INFO)
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='Logger.log', encoding='utf-8', mode ='a')
    log.addHandler(handler)
    bot.logger = logger
    bot.log = log

@bot.event
async def on_message(message):
    if message.content.startswith(config["PREFIX"]):
    	await bot.process_commands(message)
@bot.event
async def on_message_edit(before, message):
    if message.content.startswith(config["PREFIX"]):
    	await bot.process_commands(message)
@bot.event
async def on_command_error(error, ctx):
    channel = ctx.message.channel
    if isinstance(error, commands.MissingRequiredArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.BadArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(channel, "✋ **That command is disabled.** ⛔")
    elif isinstance(error, commands.CommandInvokeError):
        logger.exception("Exception in command '{}'".format(
            ctx.command.qualified_name), exc_info=error.original)
        oneliner = "Error in command '{}' - {}: {}".format(
            ctx.command.qualified_name, type(error.original).__name__,
            str(error.original))
        await ctx.bot.send_message(channel, inline(oneliner))
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CheckFailure):
        pass
    elif isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(channel, "✋ That command is not "
                                        "available in DMs.")
    elif isinstance(error, commands.CommandOnCooldown):
        await bot.send_message(channel, "✋ **A command cooldown is initiated on this command."
                                        " Try again in** ***`{:.2f}`s***"
                                        "".format(error.retry_after))

    else:
        logger.exception(type(error).__name__, exc_info=error)

if config is not None:
	bot.run(config["TOKEN"])
else:
	print('No Token set.\nRun python setup.py and configure the bot.')
