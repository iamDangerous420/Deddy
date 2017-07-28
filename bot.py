import discord
import os
import sys
from discord.ext import commands
import logging
#import emoji
from collections import Counter
import json
import asyncio
import pip


def init_logging(bot):
    logging.root.setLevel(logging.INFO)
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.INFO)
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='Logger.log', encoding='utf-8', mode ='a')
    log.addHandler(handler)
    bot.logger = logger
    bot.log = log

h = "info.json"
if not os.path.exists(h):
    with open(h, "w") as f:
        writeJ = '{"PREFIX": "None", "TOKEN": "None", "GAME": "None", "DEV_MODE": "False", "FIRST_SETUP": "True", "OWNER": "None"}'
        parse = json.loads(writeJ)
        f.write(json.dumps(parse, indent=4, sort_keys=True))
        f.truncate()
        print("Created info.json\nRunning setup.py due to first launch.")
else:
    print("Starting with current info.json")

with open("info.json") as f:
    config = json.load(f)

INTERACTIVE_MODE = not len(sys.argv) > 1


win = os.name == "nt"

def wait():
    if INTERACTIVE_MODE:
        input("Press enter to continue.")


def user_choice():
    return input("> ").lower().strip()

def menu():
    while True:
        print("Options :\nType a # and i will guide you through it!")
        print("1. Set Bot Token")
        print("2. Set The Bots Global Prefix")
        print("3. Set Bot Owner ID")
        print("4. Install Requirements")
        print("5. Login game.")
        print("6. Developer mode.")
        print("0. Run Bot")

        choice = user_choice()
        if choice == "1":
            with open(h, "r+"   ) as f:
                configg = json.load(f)
                token = input("Please paste your application token here: ")
                configg["TOKEN"] = token
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
                print("Successfully set the token.")
                wait()
        elif choice == "2":
            with open(h, "r+") as f:
                configg = json.load(f)
                prefix = input("Type your prefered prefix for your bot: ")
                configg["PREFIX"] = prefix
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
                print("Global Prefix Set!")
                wait()
        elif choice == "3":
            with open(h, "r+") as f:
                configg = json.load(f)
                id = input("Paste The Owner ID: ")
                configg["OWNER"] = id
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
                print("Owner Id set!")
                wait()
        elif choice == "4":
            pip.main(['install', '-r', "req.txt"])
            wait()
        elif choice == "5":
            with open(h, "r+") as f:
                configg = json.load(f)
                g = input("Paste The playing stats ypu would like to view as so as i login: ")
                configg["GAME"] = g
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
                print("Playing status set!")
                wait()
        elif choice == "6":
            with open(h, "r+") as f:
                configg = json.load(f)
                d = input("Type True to enable or false to disable dév mode.: ")
                configg["DEV_MODE"] = d
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
                print("Developer status set!")
                wait()
        #elif choice == "5":
            #python bot.py
        elif choice == "0":
            break
        if win:
            os.system("cls")
        else:
            os.system("clear")

initial_extensions = [
    'modules.repl',
    #'modules.tokens',
    'modules.dv'
    ]

description = '''A Bot Made by Teddy And Dangerous through Discord.py.'''

class deddy(commands.Bot):
    def __init__(self, *args, **kwargs):
        command_prefix= kwargs.pop('command_prefix', commands.when_mentioned_or(config["PREFIX"]))
        init_logging(self)
        super().__init__(command_prefix=command_prefix, *args, **kwargs)



    async def on_ready(self):
        users = len(set(self.get_all_members()))
        servers = len(self.servers)
        channels = len([c for c in self.get_all_channels()])
        if config["GAME"] == "None":
            config["GAME"] = '{}help | #Deddy'.format(config["PREFIX"])
            d = '(DEFAULT)'
        else:
            config["GAME"] = config["GAME"]
            d = '(CUSTOM)'

        if config["TOKEN"] is not None and config["OWNER"] is None:
            data = await self.application_info()
            with open(h, "r+") as f:
                configg = json.load(f)
                configg["OWNER"] = data.owner.id
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
        print('+-------------Deddy-------------+')
        print('Logged in as : \n{}({})'.format(self.user.name,self.user.id))
        print('Current prefix : {}'.format(config["PREFIX"]))
        print('Developer status set to : {}'.format(config["DEV_MODE"]))
        await self.change_presence(game=discord.Game(name=config["GAME"], status=None))
        print('Playing status set to : {} {}'.format(config["GAME"], d))
        print('+------Current Statistics------+')
        #print('')
        print("{} servers".format(servers))
        print("{} channels".format(channels))
        print("{} users".format(users))
        print('_-----------------------------_')
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith(config["PREFIX"]):
            await self.process_commands(message)

        await self.process_commands(message)

    async def on_message_edit(before, message):
        if message.author.bot:
            return
        if message.content.startswith(config["PREFIX"]):
            await bot.process_commands(message)

    async def on_command_error(self, error, ctx):
        channel = ctx.message.channel
        if isinstance(error, commands.MissingRequiredArgument):
            await send_cmd_help(ctx)
        elif isinstance(error, commands.BadArgument):
            await send_cmd_help(ctx)
        elif isinstance(error, commands.DisabledCommand):
            await self.send_message(channel, "✋ **That command is disabled.** ⛔")
        elif isinstance(error, commands.CommandInvokeError):
            logger.exception("Exception in command '{}'".format(
                ctx.command.qualified_name), exc_info=error.original)
            oneliner = "Error in command '{}' - {}: {}".format(
                ctx.command.qualified_name, type(error.original).__name__,
                str(error.original))
            await ctx.self.send_message(channel, inline(oneliner))
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.NoPrivateMessage):
            await self.send_message(channel, "✋ That command is not "
                                            "available in DMs.")
        elif isinstance(error, commands.CommandOnCooldown):
            await self.send_message(channel, "✋ **A command cooldown is initiated on this command."
                                            " Try again in** ***`{:.2f}`s***"
                                            "".format(error.retry_after))

        else:
            pass

bot = deddy(description=description, pm_help=True)
if __name__ == '__main__':
    #loop = asyncio.get_event_loop()
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    if config is not None:
        if config["FIRST_SETUP"] == "True":
            with open(h, "r+") as f:
                configg = json.load(f)
                configg["FIRST_SETUP"] = "False"
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
            print("First Setup initiated.")
            menu()

        if config["PREFIX"] == "None":
            print('No Prefix set.\nMemu time!.')
            with open(h, "r+") as f:
                configg = json.load(f)
                prefix = input("Type your prefered prefix for your bot: ")
                configg["PREFIX"] = prefix
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
                print("Global Prefix Set! Pls Wait 1s")
                asyncio.sleep(1)
                input("Press enter to start your bot.")
        else:
            pass
    if config["TOKEN"] == "None":
        print('No Token set.\nMemu time!.')
        menu()
        asyncio.sleep(1)
    else:
        try:
            bot.run(config["TOKEN"])
        except discord.LoginFailure:
            print("\nLogin Failure experienced possibly due to an invalid token.\nPlease Reconfigure your bot.")
            menu()

