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

battle_royale = discord.PartialEmoji(id=1086000463775797348, name="battle_royale")

class BelowTaskDoneButton(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(custom_id="yes", label="Yess!", style=discord.ButtonStyle.green)
    async def yes(self, ctx:discord.Interaction, button: discord.ui.button):
        
        message = discord.Embed(description=f"❌ Ticket will be deleted in few seconds",color=0xcd0e0e)
        await ctx.channel.send(embed=message)
        await asyncio.sleep(10)
        await ctx.channel.delete()

class TopTaskDoneButton(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(custom_id="done", label="Done", style=discord.ButtonStyle.green, emoji='✅')
    async def done(self, ctx:discord.Interaction, button: discord.ui.button):
        
        ticket_id = int(ctx.channel.topic)
        guild = ctx.guild
        officer =get(guild.roles, id=881749441734914100)
        admin =get(guild.roles, id=881748359134732288)

        if ctx.user.id == ticket_id or officer in ctx.user.roles or admin in ctx.user.roles:
            err=discord.Embed(description=f"{ctx.user} You sure?",color=0xcd0e0e)
            await ctx.response.send_message(embed=err, ephemeral=True, view=BelowTaskDoneButton())
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err)
    
class TasksButtons(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(custom_id="battle_royale", label="Battle Royale", style=discord.ButtonStyle.blurple, emoji='<:battle_royale_icon:1086260356453761054>')
    async def battle_royale(self, ctx:discord.Interaction, button: discord.ui.button):
        
        # # Database and misc.
        guild = ctx.guild
        with open("./obey database/help_indexing.json", "r") as f:
            index = json.load(f)
            royale = index["royale"]
            ticket_ebt = int(royale) + 1

        # # number prefixing
        if len(str(ticket_ebt)) == 1:
            ticket_prefix = "000"
        if len(str(ticket_ebt)) == 2:
            ticket_prefix = "00"
        if len(str(ticket_ebt)) == 3:
            ticket_prefix = "0"
        if len(str(ticket_ebt)) == 4:
            ticket_prefix = ""

        # # Full ticket name (name, number)
        full_ticket = f"royale-{ticket_prefix}{int(royale) + 1}"

        # # Category for creating tickets
        category = discord.utils.get(ctx.guild.categories, id=1085983572436992061)

        # # roles define and overwrites for these roles
        officer =get(guild.roles, id=881749441734914100)
        clan_member =get(guild.roles, id=881330782185074718)
        ally =get(guild.roles, id=989171283348574268)
        helper =get(guild.roles, id=980100979171151922)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            clan_member: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            ally: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            helper: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
        }

        # # Ticket Creation
        ticket_channel = await ctx.guild.create_text_channel(name=full_ticket, category=category, overwrites=overwrites, topic=(ctx.user.id))

        done = discord.Embed(description=f"Successfully created ticket at {ticket_channel.mention}")
        await ctx.response.send_message(embed=done, ephemeral=True)

        ticket_message = discord.Embed(description=f"Hello {ctx.user.mention} explain your task **below**\n\nTask category: **Battle Royale**")
        await ticket_channel.send(f"User",embed=ticket_message, view=TopTaskDoneButton())

        with open("./obey database/help_indexing.json", "w") as f:
            index.update({"royale":str(ticket_ebt)})
            json.dump(index, f)
    
    @discord.ui.button(custom_id="flags", label="Flag Capture", style=discord.ButtonStyle.blurple, emoji='<:Mode_flag_icon:1086287879057182841>')
    async def flags(self, ctx:discord.Interaction, button: discord.ui.button):
        # # Database and misc.
        guild = ctx.guild
        with open("./obey database/help_indexing.json", "r") as f:
            index = json.load(f)
            flags = index["flags"]
            ticket_ebt = int(flags) + 1

        # # number prefixing
        if len(str(ticket_ebt)) == 1:
            ticket_prefix = "000"
        if len(str(ticket_ebt)) == 2:
            ticket_prefix = "00"
        if len(str(ticket_ebt)) == 3:
            ticket_prefix = "0"
        if len(str(ticket_ebt)) == 4:
            ticket_prefix = ""

        # # Full ticket name (name, number)
        full_ticket = f"flags-{ticket_prefix}{int(ticket_ebt)}"

        # # Category for creating tickets
        category = discord.utils.get(ctx.guild.categories, id=1085983572436992061)

        # # roles define and overwrites for these roles
        officer =get(guild.roles, id=881749441734914100)
        clan_member =get(guild.roles, id=881330782185074718)
        ally =get(guild.roles, id=989171283348574268)
        helper =get(guild.roles, id=980100979171151922)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            clan_member: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            ally: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            helper: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
        }

        # # Ticket Creation
        ticket_channel = await ctx.guild.create_text_channel(name=full_ticket, category=category, overwrites=overwrites, topic=(ctx.user.id))

        done = discord.Embed(description=f"Successfully created ticket at {ticket_channel.mention}")
        await ctx.response.send_message(embed=done, ephemeral=True)

        ticket_message = discord.Embed(description=f"Hello {ctx.user.mention} explain your task **below**\n\nTask category: **Flag Capture**")
        await ticket_channel.send(f"User",embed=ticket_message, view=TopTaskDoneButton())

        with open("./obey database/help_indexing.json", "w") as f:
            index.update({"flags":str(ticket_ebt)})
            json.dump(index, f)

    @discord.ui.button(custom_id="point", label="Point Capture", style=discord.ButtonStyle.blurple, emoji='<:point_capture:1086293379463270470>')
    async def point(self, ctx:discord.Interaction, button: discord.ui.button):
        # # Database and misc.
        guild = ctx.guild
        with open("./obey database/help_indexing.json", "r") as f:
            index = json.load(f)
            point = index["point"]
            ticket_ebt = int(point) + 1

        # # number prefixing
        if len(str(ticket_ebt)) == 1:
            ticket_prefix = "000"
        if len(str(ticket_ebt)) == 2:
            ticket_prefix = "00"
        if len(str(ticket_ebt)) == 3:
            ticket_prefix = "0"
        if len(str(ticket_ebt)) == 4:
            ticket_prefix = ""

        # # Full ticket name (name, number)
        full_ticket = f"pointcapture-{ticket_prefix}{int(ticket_ebt)}"

        # # Category for creating tickets
        category = discord.utils.get(ctx.guild.categories, id=1085983572436992061)

        # # roles define and overwrites for these roles
        officer =get(guild.roles, id=881749441734914100)
        clan_member =get(guild.roles, id=881330782185074718)
        ally =get(guild.roles, id=989171283348574268)
        helper =get(guild.roles, id=980100979171151922)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            clan_member: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            ally: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            helper: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
        }

        # # Ticket Creation
        ticket_channel = await ctx.guild.create_text_channel(name=full_ticket, category=category, overwrites=overwrites, topic=(ctx.user.id))

        done = discord.Embed(description=f"Successfully created ticket at {ticket_channel.mention}")
        await ctx.response.send_message(embed=done, ephemeral=True)

        ticket_message = discord.Embed(description=f"Hello {ctx.user.mention} explain your task **below**\n\nTask category: **Point Capture**")
        await ticket_channel.send(f"User",embed=ticket_message, view=TopTaskDoneButton())

        with open("./obey database/help_indexing.json", "w") as f:
            index.update({"point":str(ticket_ebt)})
            json.dump(index, f)
    
    @discord.ui.button(custom_id="ts", label="Team Strike", style=discord.ButtonStyle.blurple, emoji='<:teamstrike:1086292243477954571>')
    async def teamstrike(self, ctx:discord.Interaction, button: discord.ui.button):
        # # Database and misc.
        guild = ctx.guild
        with open("./obey database/help_indexing.json", "r") as f:
            index = json.load(f)
            ts = index["ts"]
            ticket_ebt = int(ts) + 1

        # # number prefixing
        if len(str(ticket_ebt)) == 1:
            ticket_prefix = "000"
        if len(str(ticket_ebt)) == 2:
            ticket_prefix = "00"
        if len(str(ticket_ebt)) == 3:
            ticket_prefix = "0"
        if len(str(ticket_ebt)) == 4:
            ticket_prefix = ""

        # # Full ticket name (name, number)
        full_ticket = f"teamstrike-{ticket_prefix}{int(ticket_ebt)}"

        # # Category for creating tickets
        category = discord.utils.get(ctx.guild.categories, id=1085983572436992061)

        # # roles define and overwrites for these roles
        officer =get(guild.roles, id=881749441734914100)
        clan_member =get(guild.roles, id=881330782185074718)
        ally =get(guild.roles, id=989171283348574268)
        helper =get(guild.roles, id=980100979171151922)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            clan_member: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            ally: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            helper: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
        }

        # # Ticket Creation
        ticket_channel = await ctx.guild.create_text_channel(name=full_ticket, category=category, overwrites=overwrites, topic=(ctx.user.id))

        done = discord.Embed(description=f"Successfully created ticket at {ticket_channel.mention}")
        await ctx.response.send_message(embed=done, ephemeral=True)

        ticket_message = discord.Embed(description=f"Hello {ctx.user.mention} explain your task **below**\n\nTask category: **Team Strike**")
        await ticket_channel.send(f"User",embed=ticket_message, view=TopTaskDoneButton())

        with open("./obey database/help_indexing.json", "w") as f:
            index.update({"ts":str(ticket_ebt)})
            json.dump(index, f)

    @discord.ui.button(custom_id="siege", label="Siege", style=discord.ButtonStyle.blurple, emoji='<:gamemode_siege:1086302748846338069>')
    async def siege(self, ctx:discord.Interaction, button: discord.ui.button):
        # # Database and misc.
        guild = ctx.guild
        with open("./obey database/help_indexing.json", "r") as f:
            index = json.load(f)
            siege = index["siege"]
            ticket_ebt = int(siege) + 1

        # # number prefixing
        if len(str(ticket_ebt)) == 1:
            ticket_prefix = "000"
        if len(str(ticket_ebt)) == 2:
            ticket_prefix = "00"
        if len(str(ticket_ebt)) == 3:
            ticket_prefix = "0"
        if len(str(ticket_ebt)) == 4:
            ticket_prefix = ""

        # # Full ticket name (name, number)
        full_ticket = f"siege-{ticket_prefix}{int(ticket_ebt)}"

        # # Category for creating tickets
        category = discord.utils.get(ctx.guild.categories, id=1085983572436992061)

        # # roles define and overwrites for these roles
        officer =get(guild.roles, id=881749441734914100)
        clan_member =get(guild.roles, id=881330782185074718)
        ally =get(guild.roles, id=989171283348574268)
        helper =get(guild.roles, id=980100979171151922)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            clan_member: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            ally: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            helper: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
        }

        # # Ticket Creation
        ticket_channel = await ctx.guild.create_text_channel(name=full_ticket, category=category, overwrites=overwrites, topic=(ctx.user.id))

        done = discord.Embed(description=f"Successfully created ticket at {ticket_channel.mention}")
        await ctx.response.send_message(embed=done, ephemeral=True)

        ticket_message = discord.Embed(description=f"Hello {ctx.user.mention} explain your task **below**\n\nTask category: **Siege**")
        await ticket_channel.send(f"User",embed=ticket_message, view=TopTaskDoneButton())

        with open("./obey database/help_indexing.json", "w") as f:
            index.update({"siege":str(ticket_ebt)})
            json.dump(index, f)

    @discord.ui.button(custom_id="raids", label="Raid", style=discord.ButtonStyle.blurple, emoji='<:raids:1086289967262740521>')
    async def raids(self, ctx:discord.Interaction, button: discord.ui.button):
        # # Database and misc.
        guild = ctx.guild
        with open("./obey database/help_indexing.json", "r") as f:
            index = json.load(f)
            flags = index["flags"]
            ticket_ebt = int(flags) + 1

        # # number prefixing
        if len(str(ticket_ebt)) == 1:
            ticket_prefix = "000"
        if len(str(ticket_ebt)) == 2:
            ticket_prefix = "00"
        if len(str(ticket_ebt)) == 3:
            ticket_prefix = "0"
        if len(str(ticket_ebt)) == 4:
            ticket_prefix = ""

        # # Full ticket name (name, number)
        full_ticket = f"raid-{ticket_prefix}{int(ticket_ebt)}"

        # # Category for creating tickets
        category = discord.utils.get(ctx.guild.categories, id=1085983572436992061)

        # # roles define and overwrites for these roles
        officer =get(guild.roles, id=881749441734914100)
        clan_member =get(guild.roles, id=881330782185074718)
        ally =get(guild.roles, id=989171283348574268)
        helper =get(guild.roles, id=980100979171151922)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            clan_member: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            ally: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            helper: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
        }

        # # Ticket Creation
        ticket_channel = await ctx.guild.create_text_channel(name=full_ticket, category=category, overwrites=overwrites, topic=(ctx.user.id))

        done = discord.Embed(description=f"Successfully created ticket at {ticket_channel.mention}")
        await ctx.response.send_message(embed=done, ephemeral=True)

        ticket_message = discord.Embed(description=f"Hello {ctx.user.mention} explain your task **below**\n\nTask category: **Flag Capture**")
        await ticket_channel.send(f"User",embed=ticket_message, view=TopTaskDoneButton())

        with open("./obey database/help_indexing.json", "w") as f:
            index.update({"raids":str(ticket_ebt)})
            json.dump(index, f)

    @discord.ui.button(custom_id="invisible_kills", label="Invisible Kills", style=discord.ButtonStyle.blurple, emoji="<:stealth_bracelet:1086262306004025375>")
    async def invis(self, ctx:discord.Interaction, button: discord.ui.button):

        # # Database and misc.
        guild = ctx.guild
        with open("./obey database/help_indexing.json", "r") as f:
            index = json.load(f)
            invis = index["invis"]
            ticket_ebt = int(invis) + 1

        # # number prefixing
        if len(str(ticket_ebt)) == 1:
            ticket_prefix = "000"
        if len(str(ticket_ebt)) == 2:
            ticket_prefix = "00"
        if len(str(ticket_ebt)) == 3:
            ticket_prefix = "0"
        if len(str(ticket_ebt)) == 4:
            ticket_prefix = ""

        # # Full ticket name (name, number)
        full_ticket = f"invisible_kills-{ticket_prefix}{int(ticket_ebt)}"

        # # Category for creating tickets
        category = discord.utils.get(ctx.guild.categories, id=1085983572436992061)

        # # roles define and overwrites for these roles
        officer =get(guild.roles, id=881749441734914100)
        clan_member =get(guild.roles, id=881330782185074718)
        ally =get(guild.roles, id=989171283348574268)
        helper =get(guild.roles, id=980100979171151922)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            clan_member: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            ally: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            helper: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
        }

        # # Ticket Creation
        ticket_channel = await ctx.guild.create_text_channel(name=full_ticket, category=category, overwrites=overwrites, topic=(ctx.user.id))

        done = discord.Embed(description=f"Successfully created ticket at {ticket_channel.mention}")
        await ctx.response.send_message(embed=done, ephemeral=True)

        ticket_message = discord.Embed(description=f"Hello {ctx.user.mention} explain your task **below**\n\nTask category: **Invisible Kills**")
        await ticket_channel.send(f"User",embed=ticket_message, view=TopTaskDoneButton())

        with open("./obey database/help_indexing.json", "w") as f:
            index.update({"invis":str(ticket_ebt)})
            json.dump(index, f)

    @discord.ui.button(custom_id="wall", label="Kills through the wall", style=discord.ButtonStyle.blurple, emoji='<:final_verdict:1086267546828800074>')
    async def wall(self, ctx:discord.Interaction, button: discord.ui.button):

        # # Database and misc.
        guild = ctx.guild
        with open("./obey database/help_indexing.json", "r") as f:
            index = json.load(f)
            wall = index["wall"]
            ticket_ebt = int(wall) + 1

        # # number prefixing
        if len(str(ticket_ebt)) == 1:
            ticket_prefix = "000"
        if len(str(ticket_ebt)) == 2:
            ticket_prefix = "00"
        if len(str(ticket_ebt)) == 3:
            ticket_prefix = "0"
        if len(str(ticket_ebt)) == 4:
            ticket_prefix = ""

        # # Full ticket name (name, number)
        full_ticket = f"wallbreak-{ticket_prefix}{int(ticket_ebt)}"

        # # Category for creating tickets
        category = discord.utils.get(ctx.guild.categories, id=1085983572436992061)

        # # roles define and overwrites for these roles
        officer =get(guild.roles, id=881749441734914100)
        clan_member =get(guild.roles, id=881330782185074718)
        ally =get(guild.roles, id=989171283348574268)
        helper =get(guild.roles, id=980100979171151922)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            clan_member: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            ally: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            helper: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
        }

        # # Ticket Creation
        ticket_channel = await ctx.guild.create_text_channel(name=full_ticket, category=category, overwrites=overwrites, topic=(ctx.user.id))

        done = discord.Embed(description=f"Successfully created ticket at {ticket_channel.mention}")
        await ctx.response.send_message(embed=done, ephemeral=True)

        ticket_message = discord.Embed(description=f"Hello {ctx.user.mention} explain your task **below**\n\nTask category: **Kills through the wall**")
        await ticket_channel.send(f"User",embed=ticket_message, view=TopTaskDoneButton())

        with open("./obey database/help_indexing.json", "w") as f:
            index.update({"wall":str(ticket_ebt)})
            json.dump(index, f)

    @discord.ui.button(custom_id="chest", label="Chest Trade", style=discord.ButtonStyle.blurple, emoji='<:chest_3:1086294840230301876>')
    async def chesttrade(self, ctx:discord.Interaction, button: discord.ui.button):

        # # Database and misc.
        guild = ctx.guild
        with open("./obey database/help_indexing.json", "r") as f:
            index = json.load(f)
            chest = index["chest"]
            ticket_ebt = int(chest) + 1

        # # number prefixing
        if len(str(ticket_ebt)) == 1:
            ticket_prefix = "000"
        if len(str(ticket_ebt)) == 2:
            ticket_prefix = "00"
        if len(str(ticket_ebt)) == 3:
            ticket_prefix = "0"
        if len(str(ticket_ebt)) == 4:
            ticket_prefix = ""

        # # Full ticket name (name, number)
        full_ticket = f"chest_trade-{ticket_prefix}{int(ticket_ebt)}"

        # # Category for creating tickets
        category = discord.utils.get(ctx.guild.categories, id=1085983572436992061)

        # # roles define and overwrites for these roles
        officer =get(guild.roles, id=881749441734914100)
        clan_member =get(guild.roles, id=881330782185074718)
        ally =get(guild.roles, id=989171283348574268)
        helper =get(guild.roles, id=980100979171151922)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            clan_member: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            ally: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            helper: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
        }

        # # Ticket Creation
        ticket_channel = await ctx.guild.create_text_channel(name=full_ticket, category=category, overwrites=overwrites, topic=(ctx.user.id))

        done = discord.Embed(description=f"Successfully created ticket at {ticket_channel.mention}")
        await ctx.response.send_message(embed=done, ephemeral=True)

        ticket_message = discord.Embed(description=f"Hello {ctx.user.mention} explain your task **below**\n\nTask category: **Chest Trade**")
        await ticket_channel.send(f"User",embed=ticket_message, view=TopTaskDoneButton())

        with open("./obey database/help_indexing.json", "w") as f:
            index.update({"chest":str(ticket_ebt)})
            json.dump(index, f)
    
    @discord.ui.button(custom_id="squad", label="Squad", style=discord.ButtonStyle.blurple, emoji='<:squad_image:1086266219247702026>')
    async def squad(self, ctx:discord.Interaction, button: discord.ui.button):

        # # Database and misc.
        guild = ctx.guild
        with open("./obey database/help_indexing.json", "r") as f:
            index = json.load(f)
            squad = index["squad"]
            ticket_ebt = int(squad) + 1

        # # number prefixing
        if len(str(ticket_ebt)) == 1:
            ticket_prefix = "000"
        if len(str(ticket_ebt)) == 2:
            ticket_prefix = "00"
        if len(str(ticket_ebt)) == 3:
            ticket_prefix = "0"
        if len(str(ticket_ebt)) == 4:
            ticket_prefix = ""

        # # Full ticket name (name, number)
        full_ticket = f"squad-{ticket_prefix}{int(ticket_ebt)}"

        # # Category for creating tickets
        category = discord.utils.get(ctx.guild.categories, id=1085983572436992061)

        # # roles define and overwrites for these roles
        officer =get(guild.roles, id=881749441734914100)
        clan_member =get(guild.roles, id=881330782185074718)
        ally =get(guild.roles, id=989171283348574268)
        helper =get(guild.roles, id=980100979171151922)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            clan_member: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            ally: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            helper: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
        }

        # # Ticket Creation
        ticket_channel = await ctx.guild.create_text_channel(name=full_ticket, category=category, overwrites=overwrites, topic=(ctx.user.id))

        done = discord.Embed(description=f"Successfully created ticket at {ticket_channel.mention}")
        await ctx.response.send_message(embed=done, ephemeral=True)

        ticket_message = discord.Embed(description=f"Hello {ctx.user.mention} explain your task **below**\n\nTask category: **Squad**")
        await ticket_channel.send(f"User",embed=ticket_message, view=TopTaskDoneButton())

        with open("./obey database/help_indexing.json", "w") as f:
            index.update({"squad":str(ticket_ebt)})
            json.dump(index, f)

    @discord.ui.button(custom_id="others", label="Others..", style=discord.ButtonStyle.gray, emoji='<:final_verdict:1086267546828800074>')
    async def other(self, ctx:discord.Interaction, button: discord.ui.button):
        # # Database and misc.
        guild = ctx.guild
        with open("./obey database/help_indexing.json", "r") as f:
            index = json.load(f)
            other = index["other"]
            ticket_ebt = int(other) + 1

        # # number prefixing
        if len(str(ticket_ebt)) == 1:
            ticket_prefix = "000"
        if len(str(ticket_ebt)) == 2:
            ticket_prefix = "00"
        if len(str(ticket_ebt)) == 3:
            ticket_prefix = "0"
        if len(str(ticket_ebt)) == 4:
            ticket_prefix = ""

        # # Full ticket name (name, number)
        full_ticket = f"other-{ticket_prefix}{int(ticket_ebt)}"

        # # Category for creating tickets
        category = discord.utils.get(ctx.guild.categories, id=1085983572436992061)

        # # roles define and overwrites for these roles
        officer =get(guild.roles, id=881749441734914100)
        clan_member =get(guild.roles, id=881330782185074718)
        ally =get(guild.roles, id=989171283348574268)
        helper =get(guild.roles, id=980100979171151922)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            clan_member: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            ally: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
            helper: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
        }

        # # Ticket Creation
        ticket_channel = await ctx.guild.create_text_channel(name=full_ticket, category=category, overwrites=overwrites, topic=(ctx.user.id))

        done = discord.Embed(description=f"Successfully created ticket at {ticket_channel.mention}")
        await ctx.response.send_message(embed=done, ephemeral=True)

        ticket_message = discord.Embed(description=f"Hello {ctx.user.mention} explain your task **below**\n\nTask category: **Other**")
        await ticket_channel.send(f"User",embed=ticket_message, view=TopTaskDoneButton())

        with open("./obey database/help_indexing.json", "w") as f:
            index.update({"other":str(ticket_ebt)})
            json.dump(index, f)

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="member list")
    async def test_help(self, ctx: discord.Interaction):
        

        guild = ctx.guild
        officer =get(guild.roles, id=881749441734914100)
        clan_member =get(guild.roles, id=881330782185074718)
        ally =get(guild.roles, id=989171283348574268)
        helper =get(guild.roles, id=980100979171151922)

        
        obey_clan_bot = guild.get_member(1032359513673707591)
        pfp = obey_clan_bot.display_avatar

        if ctx.user.guild_permissions.administrator:
            embed = discord.Embed(title="Here you can get help with your clan tasks!", description=f"Below you can create ticket which will be created below this channel\n\n**Every** user with roles:\n{clan_member.mention}\n{ally.mention}\n{helper.mention}\nhas access to ticket you created, so they will be able to help you!\n\nBelow you have buttons for each task category in the clan, please click clan task category you have - it will make it easier to find the category faster by helpers\n\n**__DO NOT MAKE TROLL TICKETS__**", color=0xd80e4a)
            embed.set_author(name="Obey Ticketing System",icon_url=pfp)

            await ctx.channel.send(embed=embed , view=TasksButtons())
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err, ephemeral=True)

async def setup(client):
    await client.add_cog(Test(client))
