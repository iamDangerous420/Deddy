import discord
from discord.ext import commands
import json
from dataIO import dataIO, fileIO
import logging
import time, os

log = logging.getLogger("name of logs here")

class _main:
    def __init__(self, bot):
        self.bot = bot
        self.tk = []
        self.tk_get = {}
        self.leaderboard = dataIO.load_json("data/leaderboard.json")
        self.cooldown = 60


    @commands.command(name="tokens", pass_context=True)
    async def _tokens(self, ctx, user: discord.Member=None):
        if not user:
            user = ctx.message.author
            if self.joined(user.id):
                await self.bot.say("{} you are rank {} and you have {}".format(user.id, self.get_ranked(user.id), self.get_tokens(user.id)))
            else:
                await self.bot.say("you don't have any tokens.")
        else:
            if self.joined(user.id):
                tokens = self.get_tokens(user.id)
                ranked = self.get_ranked(user.id)
                await self.bot.say("{} you ranked {} with {} tokens".format(user.name, self.get_ranked(user.id), self.get_tokens(user.id)))


    def on_message(self, message, user: discord.Member=None):
        if not user:
            user = message.author
            if user.id not in self.leaderboard:
                self.leaderboard['user.id'] = {"name" : user.name, "ranked" : 0, "tokens" : 0}
                dataIO.save_json("data/leaderboard.json", self.leaderboard)
                log.debug("{}has joined the Levelboard!".format(user.name))
            else:
                pass
        else:
            return

    def joined(self, id):
        if id in self.leaderboard:
            return True
        else:
            return False

    async def _gaintoken(self, message):
        user = message.author
        id = user.id
        if self.joined(id):
            if id in self.tk_get:
                sec = abs(self.tk_get[id] - int(time.perf_counter()))
                if sec >= self.cooldown:
                    self.add_token(id)
                    self.tk_get[id] = int(time.perf_counter())
                    fileIO("data/leaderboard.json", "save", self.leaderboard)
                if self.leaderboard[user.id]["tokens"] >= self.tk_get(self.leaderboard[user.id]["ranked"]):
                    self.leaderboard[user.id]["ranked"] += 1
                    self.leaderboard[user.id]["tokens"] = 0
                    fileIO("data/leaderboard.json")
        else:
            self.add_token(id)
            self.leaderboard[id] = int(time.perf_counter())
            fileIO("data/leaderboard.json", "save", self.leaderboard)


    def add_token(self, id):
        if self.joined(id):
            self.leaderboard[id]["tokens"] += 1

    def get_tokens(self, id):
        if self.joined(id):
            return self.leaderboard["id"]["tokens"]

    def get_ranked(self, id):
        if self.joined(id):
            return self.leaderboard["id"]["ranked"]


def check_folders():
    if not os.path.exists("data"):
        os.mkdir("data")


def check_files():
    a = "data/leaderboard.json"
    if not dataIO.is_valid_json(a):
        dataIO.save_json(a, {})


def setup(bot):
    check_files()
    check_folders()
    m = _main
    bot.add_listener(m._gaintoken, "on_message")
    bot.add_cog(m)






