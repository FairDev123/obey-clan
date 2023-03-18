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
from obeycogs.search import MemberList

class Pagination(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(custom_id="prev-ally", style=discord.ButtonStyle.green, emoji="⬅️")
    async def prev_ally(self, ctx:discord.Interaction, button: discord.ui.button):
        
        with open("./obey database/clan_allies.json", "r") as f:
            clan_allies = json.load(f)

            page = clan_allies["page"]
            names = clan_allies["names"]
            clan_ids = clan_allies["id"]
            pfps = clan_allies["pfp"]
            images = clan_allies["image"]

        if page != 0:
            page = page - 1
        else:
            page = len(names) - 1
        clan_name = names[page]
        clan_id = clan_ids[page]
        pfp = pfps[page]
        image = images[page]

        ally = discord.Embed(title=clan_name, description=f"**ID**:{clan_id}", color=0xd80e4a)
        ally.set_thumbnail(url=pfp)
        ally.set_image(url=image)
        ally.set_footer(text=f"Page {page + 1}/{len(names)}")
        await ctx.response.edit_message(embed=ally, view=Pagination())

        with open("./obey database/clan_allies.json", "w") as f:
            clan_allies.update({"page": page})
            json.dump(clan_allies, f)

    @discord.ui.button(custom_id="next-ally", style=discord.ButtonStyle.green, emoji="➡️")
    async def next_ally(self, ctx:discord.Interaction, button: discord.ui.button):

        with open("./obey database/clan_allies.json", "r") as f:
            clan_allies = json.load(f)
        
            page = clan_allies["page"]
            names = clan_allies["names"]
            clan_ids = clan_allies["id"]
            pfps = clan_allies["pfp"]
            images = clan_allies["image"]

        if page != (len(names) - 1):
            page = page + 1
        else:
            page = 0
        clan_name = names[page]
        clan_id = clan_ids[page]
        pfp = pfps[page]
        image = images[page]


        ally = discord.Embed(title=clan_name, description=f"**ID**:{clan_id}", color=0xd80e4a)
        ally.set_thumbnail(url=pfp)
        ally.set_image(url=image)
        ally.set_footer(text=f"Page {page + 1}/{len(names)}")
        await ctx.response.edit_message(embed=ally, view=Pagination())

        with open("./obey database/clan_allies.json", "w") as f:
            clan_allies.update({"page": page})
            json.dump(clan_allies, f)

class InfoButtons(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(custom_id="clan-nav", label="Navigation", style=discord.ButtonStyle.green, emoji="🔀")
    async def nav(self, ctx:discord.Interaction, button: discord.ui.button):


        navigation = discord.Embed(title="Clan channels navigation!", description=f"<#1084065843576586331> - important clan announcements you can't mute! Officers can ping you here if you haven't done tasks or collected income\n\n<#1013825830729830530> - a channel where, every week before the war, everyone votes whether they will be able to warstart\n\n<#904132805406122006> - reminding a clan member about income and warstart\n\n<#1081235077654118450> - channel to prove that you did the tasks, you must send proof here every day!\n\n<#1085984350589440170> - this is a channel for finding people to help you with your clan tasks. Create a ticket so that someone can help you!\n\n<#1069782720684769300> - in this channel you talk to other people from the clan and you can chill yourself", color=0xd80e4a)

        await ctx.response.send_message(embed=navigation, ephemeral=True)


    @discord.ui.button(custom_id="memberlist", label="Member List", style=discord.ButtonStyle.green, emoji="<:ObeyXBlkt:968267536703561758>")
    async def memberlist(self, ctx:discord.Interaction, button: discord.ui.button):

        clan_member = discord.utils.get(ctx.user.roles, name="Clan Member")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        not_clan = discord.utils.get(ctx.user.roles, name="|(Not In Clan Rn)")

        if admin in ctx.user.roles or officer in ctx.user.roles or clan_member in ctx.user.roles or not_clan in ctx.user.roles:
            with open("./obey database/members.json", "r") as f:
                members = json.load(f)
            with open("./obey database/member_list.json", "r") as f:
                member_list = json.load(f)

            discord_id_list = []
            for i in members:
                discord_id_list.append(i)
            with open("./obey database/member_list.json", "w") as f:
                member_list.update({"list":discord_id_list,"page":0})
                json.dump(member_list, f, indent=1)
            
            first_user = discord_id_list[0]

            discord_id = members[first_user]["discord_id"]
            ingame_id = members[first_user]["ingame_id"]
            valor = members[first_user]["valor"]
            nick = members[first_user]["nick"]
            clan_rank = members[first_user]["clan_rank"]
            joined_clan = members[first_user]["joined_at"]
            pic = members[first_user]["pic"]

            embed = discord.Embed(description=f">>> **In-game ID:**\n {ingame_id}\n\n**Valor points:**\n{valor}\n\n**Clan Rank:**\n{clan_rank}\n\n**Joined the clan:**\n{joined_clan}\n\n**Discord ID:**\n{discord_id}", color=0x4814a3)
            embed.set_author(name=nick, icon_url=pic)
            embed.set_footer(text=f"1/{len(discord_id_list)}")
            view = MemberList()
            await ctx.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(custom_id="clan-allies", label="Clan Allies", style=discord.ButtonStyle.green, emoji="<:1AAobeyxblackoutlite:968930520815775774>")
    async def allies(self, ctx:discord.Interaction, button: discord.ui.button):
        
        with open("./obey database/clan_allies.json", "r") as f:
            clan_allies = json.load(f)

            page = clan_allies["page"]
            names = clan_allies["names"]
            clan_ids = clan_allies["id"]
            pfps = clan_allies["pfp"]
            images = clan_allies["image"]

        page = 0
        clan_name = names[page]
        clan_id = clan_ids[page]
        pfp = pfps[page]
        image = images[page]

        ally = discord.Embed(title=clan_name, description=f"**ID**:{clan_id}", color=0xd80e4a)
        ally.set_thumbnail(url=pfp)
        ally.set_image(url=image)
        ally.set_footer(text=f"Page {page + 1}/{len(names)}")
        await ctx.response.send_message(embed=ally, ephemeral=True, view=Pagination())

        with open("./obey database/clan_allies.json", "w") as f:
            clan_allies.update({"page": 0})
            json.dump(clan_allies, f)


    @discord.ui.button(custom_id="war-info", label="War Info", style=discord.ButtonStyle.green, emoji="<:gamemode_siege:1086302748846338069>")
    async def clan_info(self, ctx:discord.Interaction, button: discord.ui.button):
        await ctx.response.send_message("Work in progress..", ephemeral=True)
    
class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="clan_info")
    async def clan_info(self, ctx: discord.Interaction):

        guild = ctx.guild
        
        if ctx.user.guild_permissions.administrator:
            obey_clan_bot = guild.get_member(1032359513673707591)
            pfp = obey_clan_bot.display_avatar

            task_completion = self.client.get_channel(1081235077654118450)
            info_embed = discord.Embed(title=f"<:ObeyXBlkt:968267536703561758> Welcome to Obey!", description=f"If you are new you must know that you are obligated to:\n\n- Do your **daily tasks** everyday and **send proof** to {task_completion.mention} if you are done! (**ignoring it = kick**)\n- **Helping each other** to maximize the clan valor points\n- Collect at least **5 incomes per day**\n\n**__If you need help feel free to ping or dm our clan officers!__**", color=0xd80e4a)
            info_embed.set_author(name="Obey Clan",icon_url=pfp)
            await ctx.channel.send(embed=info_embed, view=InfoButtons())
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err, ephemeral=True)

async def setup(client):
    await client.add_cog(Commands(client))