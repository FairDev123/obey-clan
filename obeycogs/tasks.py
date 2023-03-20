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

class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.restrictions_check.start()
        self.today_reset.start()

    @tasks.loop(seconds=5.0)
    async def restrictions_check(self):

        # # this task is responsible for inform staff about clan member restriction just ended

        with open("./obey database/task_map.json", "r") as f:
            task_map = json.load(f)
            channel_id = int(task_map["channel_id"])
            hours = task_map["hours"]

        channel_name = "｜⭐｜task completion"
        time_now = datetime.datetime.now()
        # 2023-03-03 14:46

        map_channel = self.client.get_channel(channel_id)
        task_channel = self.client.get_channel(1085984350589440170)
        guild = self.client.get_guild(706466887734919180)
        clan_member = get(guild.roles, id=881330782185074718)
        if (str(time_now))[11:16]==hours[0]:
            pins = await map_channel.pins()
            for i in pins:
                await i.unpin()
            embed1= discord.Embed(description = f"Get online and don't forget to send pictures of tasks done here!\nIf you need help please create ticket in {task_channel.mention}",color=0x1dd74c)
            embed2 = discord.Embed(description="ここで完了したタスクのスクリーンショットを送信してください", color=0x1dd74c)
            await map_channel.send(f"{clan_member.mention}\n__Remember that you can send only **ONE** message per 2 hours__",embed=embed1)
            await map_channel.send(embed=embed2)
            await asyncio.sleep(60)
        if (str(time_now))[11:16]==hours[1]:
            clan_channel = self.client.get_channel(1069782720684769300)
            embed1= discord.Embed(description = f"Get online and don't forget to send pictures of tasks done here!\nIf you need help please create ticket in {task_channel.mention}",color=0x1dd74c)
            embed2 = discord.Embed(description="ここで完了したタスクのスクリーンショットを送信してください", color=0x1dd74c)
            await map_channel.send(f"{clan_member.mention}",embed=embed1)
            await map_channel.send(embed=embed2)
            await asyncio.sleep(60)
        if (str(time_now))[11:16]==hours[2]:
            clan_channel = self.client.get_channel(1069782720684769300)
            embed1= discord.Embed(description = f"Get online and don't forget to send pictures of tasks done here!\nIf you need help please create ticket in {task_channel.mention}",color=0x1dd74c)
            embed2 = discord.Embed(description="ここで完了したタスクのスクリーンショットを送信してください", color=0x1dd74c)
            await map_channel.send(f"{clan_member.mention}",embed=embed1)
            await map_channel.send(embed=embed2)
            await asyncio.sleep(60)


    @tasks.loop(seconds=5.0)
    async def today_reset(self):
        
        # # this task is responsible for resseting user tickets in day to 0

        raw_time = str(datetime.datetime.now())
        time = raw_time[11:-10]

        if time=="00:00":
            with open("./obey database/ticket_users.json", "r") as f:
                ticket_users = json.load(f)

            for each in ticket_users:
                ticket_users[each]["today"] = 0

            with open("./obey database/ticket_users.json", "w") as f:
                json.dump(ticket_users, f, indent=1)
            await asyncio.sleep(60)

async def setup(client):
    await client.add_cog(Tasks(client))
