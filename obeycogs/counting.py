import discord
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, guild_only
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
import time
import requests
import json
import os
from itertools import cycle
from dateutil.relativedelta import relativedelta

class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,ctx):
        await self.client.process_commands(ctx)

        counting_channel = 1070768145167552573

        with open("./obey database/task_map.json", "r") as f:
            task_map = json.load(f)
            channel_id = int(task_map["channel_id"])
        
        if ctx.channel.id == counting_channel and ctx.id != 1032359513673707591:
                    with open("./obey database/counting.json", "r") as f:
                        counting = json.load(f)
                    if eval(ctx.content) > 0:
                        integer = eval(ctx.content)
                        number = counting["number"]
                        last = counting["last"]
                        if integer == int(number) and last != ctx.author.name:
                            await ctx.add_reaction("✅")
                            counting.update({"number":number + 1,"last":ctx.author.name})
                            with open("./obey database/counting.json", "w") as f:
                                json.dump(counting, f)
                        else:
                            await ctx.add_reaction("❌")
                            embed=discord.Embed(title="Counting",description=f"Counting resetted")
                            await ctx.channel.send(f"{ctx.author.mention} ruined it at {ctx.content}. Next number is `{number}`", embed=embed)
                            counting.update({"number":1,"last":None})
                            with open("./obey database/counting.json", "w") as f:
                                json.dump(counting, f)
        if ctx.channel.id == channel_id and ctx.author.id != 1032359513673707591:
            if ctx.attachments:
                guild = self.client.get_guild(706466887734919180)
                clan_member =get(guild.roles, id=881330782185074718)
                await ctx.pin()
            else:
                await ctx.delete()
             

    @app_commands.command()
    async def send_message(self, ctx: discord.Interaction, thing_to_say:str=None) -> None:
        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
        if admin in ctx.user.roles or officer in ctx.user.roles:
            if thing_to_say != None:
                    await ctx.channel.send(thing_to_say)
            else:
                await ctx.response.send_message("You must say something to send it to text channel")                 

async def setup(client):
    await client.add_cog(Counting(client))
