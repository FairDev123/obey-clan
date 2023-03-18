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

class ServerTrifles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="simple inrole app command by Fairshooter")
    async def inrole(self, ctx: discord.Interaction, role: discord.Role):
        if len(role.members) > 0:
            text = "\n".join(str(member.mention) for member in role.members)
            embed = discord.Embed(title=f"All user with {role} role",description=text, color=0x4814a3)
            await ctx.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title=f"No users found with {role} role!", color=0x4814a3)
            await ctx.response.send_message(embed=embed)

    @app_commands.command(description="This command send in-game clan id")
    async def clan_id(self, ctx: discord.Interaction):
        await ctx.response.send_message("21518341")

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="clan obey log")
    async def log(self, ctx: discord.Interaction, czas:int = 0, id:int = 0):
        my_date = datetime.datetime.now() + relativedelta(months = czas)
        await ctx.response.send_message(my_date)

    @app_commands.command(description="this command adding user to clan members database without restriction logger")
    @app_commands.choices(clan_rank=[
    Choice(name="Clan Member", value="Clan Member"),
    Choice(name="Clan Leader", value="Clan Leader"),
    Choice(name="Clan Co-Leader", value="Clan Co-Leader"),
    Choice(name="Clan Officer", value="Clan Officer"),
    Choice(name="Clan Ally", value="Clan Ally"),
    Choice(name="Helper", value="Helper"),
])
    async def rawjoin(self, ctx: discord.Interaction, member: discord.Member = None, id:int=0, clan_rank:str=""):

        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
        
        if admin in ctx.user.roles or officer in ctx.user.roles:
            with open("./obey database/members.json", "r") as f:
                members = json.load(f)

            time_now = datetime.datetime.now()
            time_after = str(time_now - datetime.timedelta(minutes=1))
            with open("./obey database/members.json", "w") as w:
                members.update({member.id:{
                "ingame_id": str(id),
                "valor": str(0),
                "clan_rank": clan_rank,
                "nick": member.name,
                "discord_id": str(member.id),
                "joined_at": time_after[0:16],
                "pic": str(member.display_avatar)
            }})
                json.dump(members, w, indent=1)
            embed=discord.Embed(description=f"✅ Added {member.name} to clan!",color=0x1f9336)
            await ctx.response.send_message(embed=embed)
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err)

    @app_commands.command(description="this command adding restriction logger functionality and set roles for user")
    @commands.has_role("Admin")
    @app_commands.choices(clan_rank=[
    Choice(name="Clan Member", value="Clan Member"),
    Choice(name="Clan Leader", value="Clan Leader"),
    Choice(name="Clan Co-Leader", value="Clan Co-Leader"),
    Choice(name="Clan Officer", value="Clan Officer"),
    Choice(name="Clan Ally", value="Clan Ally"),
    Choice(name="Helper", value="Helper"),
])
    async def join(self, ctx: discord.Interaction, member: discord.Member = None, id:int=0, clan_rank:str=""):
        
        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
        
        if admin in ctx.user.roles or officer in ctx.user.roles:
            with open("./obey database/members.json", "r") as f:
                members = json.load(f)

            if clan_rank == "":
                clan_rank = "Clan Member"

            time_now = datetime.datetime.now()
            time_after = str(time_now + datetime.timedelta(minutes=1))
            with open("./obey database/members.json", "w") as w:
                members.update({member.id:{
                "ingame_id": str(id),
                "valor": str(0),
                "clan_rank": clan_rank,
                "nick": member.name,
                "discord_id": str(member.id),
                "joined_at": time_after[0:16],
                "pic": str(member.display_avatar)
            }})
                json.dump(members, w, indent=1)
            embed=discord.Embed(description=f"✅ Added {member.name} to clan!",color=0x1f9336)
            await ctx.response.send_message(embed=embed)
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err)

    @app_commands.command(description="dm user")
    async def dm(self, ctx: discord.Interaction, member: discord.Member=None, id:int=0):
        OBEY = ctx.guild
        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")

        if admin in ctx.user.roles or officer in ctx.user.roles:
            if len(str(id)) < 5 and member!=None:
                if member!=None:
                        dm = await member.create_dm()
                        embed=discord.Embed(description=f"✅ Move your fucking ass and do your tasks",color=0x1f9336)
                        message = await dm.send(embed=embed)
                        embed=discord.Embed(description=f"✅ Message was sended to this user",color=0x1f9336)
                        await ctx.response.send_message(embed=embed)
                else:
                    embed=discord.Embed(description=f"❔ This command is responsible for direct message all low valor clan members\n\n**To edit member valor excute the following command:**\nSyntax: `/valor <clan_member> <amount>`",color=0x1f9336)
                    await ctx.response.send_message(embed=embed)
            else:
                with open("./obey database/members.json", "r") as f:
                    members = json.load(f)

                for i in members:
                    if members[i]["ingame_id"] == str(id):
                        member_id = members[i]["discord_id"]
                        member = OBEY.get_member(int(member_id))
                        dm = await member.create_dm()
                        embed=discord.Embed(description=f"✅ Move your fucking ass and do your tasks",color=0x1f9336)
                        message = await dm.send(embed=embed)
                        embed=discord.Embed(description=f"✅ Message was sended to all low valor members",color=0x1f9336)
                        await ctx.response.send_message(embed=embed)
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err)
    
    @app_commands.command(description="audit log")
    async def audit(self, ctx: discord.Interaction, member: discord.Member=None, id:int=0):
        
        async for entry in ctx.guild.audit_logs(action=discord.AuditLogAction.ban):
            text = "\n".join(f"{str(entry.user)} banned {str(entry.target)}" async for entry in ctx.guild.audit_logs(action=discord.AuditLogAction.ban))
            embed = discord.Embed(title="all bans", description=text)
        await ctx.response.send_message(embed=embed)
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        clan_member = discord.utils.get(before.roles, id=881330782185074718)
        after_list = []
        before_list = []

        for i in before.roles:
            before_list.append(str(i))
        if "Clan Member" not in before_list:
            for i in after.roles:
                after_list.append(str(i))
            if "Clan Member" in after_list:
                embed = discord.Embed(title="Added new Clanmate!", description=f"{before.mention}")
                channel = self.client.get_channel(1080523226586820699)
                await channel.send(embed=embed)
            if "⭐️| (Not In Clan Rn)" in after_list:
                embed = discord.Embed(title="Added member to waitlist!", description=f"{before.mention}")
                channel = self.client.get_channel(1080523226586820699)
                await channel.send(embed=embed)

async def setup(client):
    await client.add_cog(ServerTrifles(client))
    await client.add_cog(Moderation(client))