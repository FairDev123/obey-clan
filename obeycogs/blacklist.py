import discord
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, guild_only,CheckFailure
from discord.utils import get
from discord import File, ButtonStyle, Embed, Color
from discord.ui import Button, View
from discord import app_commands
from discord.app_commands import Choice
import datetime
import sqlite3
import random
import math
import asyncio
import time as tm
import requests
import json
import os
import calendar
from itertools import cycle
from dateutil.relativedelta import relativedelta

class BlackList(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(custom_id="1", label="<", style=discord.ButtonStyle.gray)
    async def previous(self, ctx:discord.Interaction, button: discord.ui.button):
        
        with open("./obey database/blacklist.json", "r") as f:
            blacklist = json.load(f)
            page_num = blacklist["page"]
            ids = blacklist["list"]

            page_num = page_num - 1

        if page_num>0:
            blacklist.update({"page":page_num})
            with open("./obey database/blacklist.json", "w") as f:
                json.dump(blacklist, f, indent=1)

            id = ids[page_num]

            embed = discord.Embed(title=f"ID {page_num}/{len(ids)}",description=f"**{id}**")
            await ctx.response.edit_message(embed=embed,view=BlackList())

    @discord.ui.button(custom_id="2", label=">", style=discord.ButtonStyle.gray)
    async def next(self, ctx:discord.Interaction, button: discord.ui.button):
        with open("./obey database/blacklist.json", "r") as f:
            blacklist = json.load(f)
            page_num = blacklist["page"]
            ids = blacklist["list"]

        page_num = page_num + 1

        blacklist.update({"page":page_num})
        with open("./obey database/blacklist.json", "w") as f:
            json.dump(blacklist, f, indent=1)

        id = ids[page_num - 1]
        
        embed = discord.Embed(title=f"ID {page_num + 1}/{len(ids)}",description=f"**{id}**")
        await ctx.response.edit_message(embed=embed,view=BlackList())

    @discord.ui.button(custom_id="3", label="<<", style=discord.ButtonStyle.green)
    async def first(self, ctx:discord.Interaction, button: discord.ui.button):
        with open("./obey database/blacklist.json", "r") as f:
            blacklist = json.load(f)
            ids = blacklist["list"]

        page_num = 0

        blacklist.update({"page":page_num})
        with open("./obey database/blacklist.json", "w") as f:
            json.dump(blacklist, f, indent=1)

        id = ids[page_num]

        embed = discord.Embed(title=f"ID {page_num + 1}/{len(ids)}",description=f"**{id}**")
        await ctx.response.edit_message(embed=embed,view=BlackList())

    @discord.ui.button(custom_id="4", label=">>", style=discord.ButtonStyle.green)
    async def last(self, ctx:discord.Interaction, button: discord.ui.button):
        with open("./obey database/blacklist.json", "r") as f:
            blacklist = json.load(f)
            ids = blacklist["list"]

        page_num = len(ids)

        blacklist.update({"page":page_num})
        with open("./obey database/blacklist.json", "w") as f:
            json.dump(blacklist, f, indent=1)
        
        id = ids[page_num - 1]

        embed = discord.Embed(title=f"ID {page_num}/{len(ids)}",description=f"**{id}**")
        await ctx.response.edit_message(embed=embed,view=BlackList())

class Blacklist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    @app_commands.choices(typeof=[
    Choice(name="ingame_id", value="ingame_id"),
    Choice(name="discord_id", value="discord_id")])
    async def blacklist_add(self, ctx: discord.Interaction, typeof:str="" ,content:str=""):

        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
        admin = discord.utils.get(ctx.user.roles, name="Administrator")

        if admin in ctx.user.roles or officer in ctx.user.roles or ctx.user.roles:
            with open("./obey database/blacklist.json", "r") as f:
                    blacklist = json.load(f)
                    discord_list = blacklist["discord_list"]
                    ids = blacklist["list"]
                    page = blacklist["page"]

            if typeof=="ingame_id":
                list_of_ids = content.split()
                ids.extend(list_of_ids)
            if typeof=="discord_id":
                list_of_ids = content.split()
                discord_list.extend(list_of_ids)

            blacklist.update({"list":ids, "discord_list":discord_list, "page":page})
            with open("./obey database/blacklist.json", "w") as f:
                    json.dump(blacklist, f, indent=1)
                    embed = discord.Embed(description="✅ Blacklist updated!")
                    await ctx.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.choices(typeof=[
    Choice(name="ingame_id", value="ingame_id"),
    Choice(name="discord_id", value="discord_id")])
    async def blacklist_remove(self, ctx: discord.Interaction, typeof:str="" ,content:str=""):

        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
        admin = discord.utils.get(ctx.user.roles, name="Administrator")

        if admin in ctx.user.roles or officer in ctx.user.roles or ctx.user.roles:
            with open("./obey database/blacklist.json", "r") as f:
                    blacklist = json.load(f)
                    discord_list = blacklist["discord_list"]
                    ids = blacklist["list"]
                    page = blacklist["page"]

            if typeof=="ingame_id":
                ids.remove(content)
            if typeof=="discord_id":
                discord_list.remove(content)

            blacklist.update({"list":ids, "discord_list":discord_list, "page":page})
            with open("./obey database/blacklist.json", "w") as f:
                json.dump(blacklist, f, indent=1)
                embed = discord.Embed(description="✅ Blacklist updated")
                await ctx.response.send_message(embed=embed)

    @app_commands.command()
    async def blacklist(self, ctx: discord.Interaction):

        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
        admin = discord.utils.get(ctx.user.roles, name="Administrator")

        if admin in ctx.user.roles or officer in ctx.user.roles or ctx.user.roles:
            with open("./obey database/blacklist.json", "r") as f:
                blacklist = json.load(f)
                ids = blacklist["list"]
            page_num = 1
            blacklist.update({"page":page_num})
            with open("./obey database/blacklist.json", "w") as f:
                json.dump(blacklist, f, indent=1)
            id = ids[page_num - 1]
            embed = discord.Embed(title=f"ID {page_num}/{len(ids)}",description=f"**{id}**")
            await ctx.response.send_message(embed=embed,view=BlackList())

async def setup(client):
    await client.add_cog(Blacklist(client))
