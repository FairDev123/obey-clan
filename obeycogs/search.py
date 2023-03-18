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

class MemberList(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(custom_id="first_button", label="First", style=discord.ButtonStyle.green, emoji="⏪", row=2)
    async def first(self, ctx:discord.Interaction, button: discord.ui.button):
        with open("./obey database/members.json", "r") as f:
            members = json.load(f)
        with open("./obey database/member_list.json", "r") as f:
            member_list = json.load(f)
            discord_id_list = member_list["list"]
            page = member_list["page"]
            with open("./obey database/member_list.json", "w") as f:
                member_list.update({"list":discord_id_list,"page":0})
                json.dump(member_list, f, indent=1)

            with open("./obey database/member_list.json", "r") as f:
                discord_id_list = member_list["list"]
                page = member_list["page"]

            discord_id = discord_id_list[page]

            discord_id = members[discord_id]["discord_id"]
            ingame_id = members[discord_id]["ingame_id"]
            valor = members[discord_id]["valor"]
            nick = members[discord_id]["nick"]
            clan_rank = members[discord_id]["clan_rank"]
            joined_clan = members[discord_id]["joined_at"]
            pic = members[discord_id]["pic"]

            embed = discord.Embed(description=f">>> **In-game ID:**\n {ingame_id}\n\n**Valor points:**\n{valor}\n\n**Clan Rank:**\n{clan_rank}\n\n**Joined the clan:**\n{joined_clan}\n\n**Discord ID:**\n{discord_id}", color=0x4814a3)
            embed.set_author(name=nick, icon_url=pic)
            embed.set_footer(text=f"{page + 1}/{len(discord_id_list)}")
            
            await ctx.response.edit_message(embed=embed)

    @discord.ui.button(custom_id="previous_button", label="Previous", style=discord.ButtonStyle.green, emoji="◀️", row=1)
    async def previous(self, ctx:discord.Interaction, button: discord.ui.button):
        with open("./obey database/members.json", "r") as f:
            members = json.load(f)
        with open("./obey database/member_list.json", "r") as f:
            member_list = json.load(f)
            discord_id_list = member_list["list"]
            page = member_list["page"]
        if page>0:
            with open("./obey database/member_list.json", "w") as f:
                member_list.update({"list":discord_id_list,"page":page - 1})
                json.dump(member_list, f, indent=1)

            with open("./obey database/member_list.json", "r") as f:
                discord_id_list = member_list["list"]
                page = member_list["page"]

            discord_id = discord_id_list[page]

            discord_id = members[discord_id]["discord_id"]
            ingame_id = members[discord_id]["ingame_id"]
            valor = members[discord_id]["valor"]
            nick = members[discord_id]["nick"]
            clan_rank = members[discord_id]["clan_rank"]
            joined_clan = members[discord_id]["joined_at"]
            pic = members[discord_id]["pic"]

            embed = discord.Embed(description=f">>> **In-game ID:**\n {ingame_id}\n\n**Valor points:**\n{valor}\n\n**Clan Rank:**\n{clan_rank}\n\n**Joined the clan:**\n{joined_clan}\n\n**Discord ID:**\n{discord_id}", color=0x4814a3)
            embed.set_author(name=nick, icon_url=pic)
            embed.set_footer(text=f"{page + 1}/{len(discord_id_list)}")
            
            await ctx.response.edit_message(embed=embed)

    @discord.ui.button(custom_id="next_button", label="Next", style=discord.ButtonStyle.green, emoji="▶️", row=1)
    async def next(self, ctx:discord.Interaction, button: discord.ui.button):
        with open("./obey database/members.json", "r") as f:
            members = json.load(f)
        with open("./obey database/member_list.json", "r") as f:
            member_list = json.load(f)
            discord_id_list = member_list["list"]
            page = member_list["page"]
        with open("./obey database/member_list.json", "w") as f:
            member_list.update({"list":discord_id_list,"page":page + 1})
            json.dump(member_list, f, indent=1)

        with open("./obey database/member_list.json", "r") as f:
            discord_id_list = member_list["list"]
            page = member_list["page"]

        discord_id = discord_id_list[page]

        discord_id = members[discord_id]["discord_id"]
        ingame_id = members[discord_id]["ingame_id"]
        valor = members[discord_id]["valor"]
        nick = members[discord_id]["nick"]
        clan_rank = members[discord_id]["clan_rank"]
        joined_clan = members[discord_id]["joined_at"]
        pic = members[discord_id]["pic"]

        embed = discord.Embed(description=f">>> **In-game ID:**\n {ingame_id}\n\n**Valor points:**\n{valor}\n\n**Clan Rank:**\n{clan_rank}\n\n**Joined the clan:**\n{joined_clan}\n\n**Discord ID:**\n{discord_id}", color=0x4814a3)
        embed.set_author(name=nick, icon_url=pic)
        embed.set_footer(text=f"{page + 1}/{len(discord_id_list)}")
        
        await ctx.response.edit_message(embed=embed)

    @discord.ui.button(custom_id="last_button", label="Last", style=discord.ButtonStyle.green, emoji="⏩", row=2)
    async def last(self, ctx:discord.Interaction, button: discord.ui.button):
        with open("./obey database/members.json", "r") as f:
            members = json.load(f)
        with open("./obey database/member_list.json", "r") as f:
            member_list = json.load(f)
            discord_id_list = member_list["list"]
            page = member_list["page"]
            with open("./obey database/member_list.json", "w") as f:
                member_list.update({"list":discord_id_list,"page":len(discord_id_list) - 1})
                json.dump(member_list, f, indent=1)

            with open("./obey database/member_list.json", "r") as f:
                discord_id_list = member_list["list"]
                page = member_list["page"]

            discord_id = discord_id_list[page]

            discord_id = members[discord_id]["discord_id"]
            ingame_id = members[discord_id]["ingame_id"]
            valor = members[discord_id]["valor"]
            nick = members[discord_id]["nick"]
            clan_rank = members[discord_id]["clan_rank"]
            joined_clan = members[discord_id]["joined_at"]
            pic = members[discord_id]["pic"]

            embed = discord.Embed(description=f">>> **In-game ID:**\n {ingame_id}\n\n**Valor points:**\n{valor}\n\n**Clan Rank:**\n{clan_rank}\n\n**Joined the clan:**\n{joined_clan}\n\n**Discord ID:**\n{discord_id}", color=0x4814a3)
            embed.set_author(name=nick, icon_url=pic)
            embed.set_footer(text=f"{page + 1}/{len(discord_id_list)}")
            
            await ctx.response.edit_message(embed=embed)

class MemberInfo(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Dm User", style=discord.ButtonStyle.green)
    async def dm_user(self, ctx:discord.Interaction, button: discord.ui.button):
        OBEY = ctx.guild
        with open("./obey database/last.json", "r") as f:
            last = json.load(f)
            last_id = last["last_id"]
        member = OBEY.get_member(int(last_id))

        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
    
        if admin in ctx.user.roles or officer in ctx.user.roles:
            dm = await member.create_dm()
            embed=discord.Embed(description=f"✅ Move your fucking ass and do your tasks",color=0x1f9336)
            message = await dm.send(embed=embed)
            embed=discord.Embed(description=f"✅ Message was sended to this user",color=0x1f9336)
            await ctx.response.send_message(embed=embed)
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err)

    @discord.ui.button(label="Display In-game ID", style=discord.ButtonStyle.gray)
    async def display_ingame_id(self, ctx:discord.Interaction, button: discord.ui.button):
        with open("./obey database/last.json", "r") as f:
            last = json.load(f)
            last_id = last["last_id"]

        with open("./obey database/members.json", "r") as f:
            members = json.load(f)
            display_id = members[str(last_id)]["ingame_id"]
            await ctx.response.send_message(display_id)

    @discord.ui.button(label="Ping for Income", style=discord.ButtonStyle.gray)
    async def ping_for_income(self, ctx:discord.Interaction, button: discord.ui.button):

        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
    
        if admin in ctx.user.roles or officer in ctx.user.roles:
            OBEY = ctx.guild
            with open("./obey database/last.json", "r") as f:
                last = json.load(f)
                last_id = last["last_id"]

            income_alert=discord.Embed(description=f":warning: Bro collect your income or ur die",color=0xcd0e0e)
            sucess=discord.Embed(description=f"✅ The message has been successfully sent!",color=0x1f9336)
            with open("./obey database/members.json", "r") as f:
                members = json.load(f)
                member = members[last_id]["discord_id"]
            clan_chat = self.client.get_channel(1069782720684769300)
            member = OBEY.get_member(int(last_id))
            await clan_chat.send(f"{member.mention}",embed=income_alert)
            await ctx.response.send_message(embed=sucess)
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err)

    @discord.ui.button(label="Ping for Tasks", style=discord.ButtonStyle.gray)
    async def ping_for_tasks(self, ctx:discord.Interaction, button: discord.ui.button):
        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
    
        if admin in ctx.user.roles or officer in ctx.user.roles:
            OBEY = ctx.guild
            with open("./obey database/last.json", "r") as f:
                last = json.load(f)
                last_id = last["last_id"]

            tasks_alert=discord.Embed(description=f":warning: Bro do your tasks or ur die",color=0xcd0e0e)
            sucess=discord.Embed(description=f"✅ The message has been successfully sent!",color=0x1f9336)
            with open("./obey database/members.json", "r") as f:
                members = json.load(f)
                member = members[last_id]["discord_id"]
            clan_chat = self.client.get_channel(1069782720684769300)
            member = OBEY.get_member(int(last_id))
            await clan_chat.send(f"{member.mention}",embed=tasks_alert)
            await ctx.response.send_message(embed=sucess)
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err)

    @discord.ui.button(label="Display avatar", style=discord.ButtonStyle.blurple)
    async def avatar(self, ctx:discord.Interaction, button: discord.ui.button):
        with open("./obey database/last.json", "r") as f:
            last = json.load(f)
            last_id = last["last_id"]

        with open("./obey database/members.json", "r") as f:
            members = json.load(f)
            display_avatar = members[str(last_id)]["pic"]

        await ctx.response.send_message(display_avatar)

class Search(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="info about registered clan member")
    async def search(self, ctx: discord.Interaction, member: discord.Member=None, id:int=0, discord_id:int=0,nickname:str="test"):

        OBEY = ctx.guild
        id_index = False
        discord_index = False
        with open("./obey database/members.json", "r") as f:
            members = json.load(f)

        if member!=None:
            if id==0 and str(member.id) in members:

                discord_id = str(member.id)

                pic = member.display_avatar

                if discord_id in members:
                    discord_id = members[discord_id]["discord_id"]
                    ingame_id = members[discord_id]["ingame_id"]
                    valor = members[discord_id]["valor"]
                    nick = members[discord_id]["nick"]
                    clan_rank = members[discord_id]["clan_rank"]
                    joined_clan = members[discord_id]["joined_at"]
                    embed = discord.Embed(description=f">>> **In-game ID:**\n {ingame_id}\n\n**Valor points:**\n{valor}\n\n**Clan Rank:**\n{clan_rank}\n\n**Joined the clan:**\n{joined_clan}\n\n**Discord ID:**\n{discord_id}", color=0x4814a3)
                    embed.set_author(name=nick, icon_url=pic)

                with open("./obey database/last.json", "r") as f:
                    last = json.load(f)

                with open("./obey database/last.json", "w") as f:
                    last.update({"last_id":discord_id})
                    json.dump(last, f)
                view = MemberInfo()
                await ctx.response.send_message(view=view, embed=embed)
        
        for i in members:
            if str(id) in members[i]["ingame_id"]:
                id_index = True

        if id!=0:
            if member==None and id_index == True:

                for i in members:
                    if str(id) in members[i]["ingame_id"]:
                        discord_id = members[i]["discord_id"]
                        ingame_id = members[i]["ingame_id"]
                        valor = members[i]["valor"]
                        nick = members[i]["nick"]
                        clan_rank = members[i]["clan_rank"]
                        joined_clan = members[i]["joined_at"]
                        pic = members[i]["pic"]
                        embed = discord.Embed(description=f">>> **In-game ID:**\n {ingame_id}\n\n**Valor points:**\n{valor}\n\n**Clan Rank:**\n{clan_rank}\n\n**Joined the clan:**\n{joined_clan}\n\n**Discord ID:**\n{discord_id}", color=0x4814a3)
                        embed.set_author(name=nick, icon_url=pic)

                with open("./obey database/last.json", "r") as f:
                    last = json.load(f)

                with open("./obey database/last.json", "w") as f:
                    last.update({"last_id":discord_id})
                    json.dump(last, f)
                view = MemberInfo()
                await ctx.response.send_message(view=view, embed=embed)

        for i in members:
            if str(id) in members[i]["discord_id"]:
                discord_index = True
        if discord_id!=0:
            if member==None and discord_index == True:

                for i in members:
                    if str(discord_id) in members[i]["discord_id"]:
                        discord_id = members[i]["discord_id"]
                        ingame_id = members[i]["ingame_id"]
                        valor = members[i]["valor"]
                        nick = members[i]["nick"]
                        clan_rank = members[i]["clan_rank"]
                        joined_clan = members[i]["joined_at"]
                        pic = members[i]["pic"]
                        embed = discord.Embed(description=f">>> **In-game ID:**\n {ingame_id}\n\n**Valor points:**\n{valor}\n\n**Clan Rank:**\n{clan_rank}\n\n**Joined the clan:**\n{joined_clan}\n\n**Discord ID:**\n{discord_id}", color=0x4814a3)
                        embed.set_author(name=nick, icon_url=pic)

                with open("./obey database/last.json", "r") as f:
                    last = json.load(f)

                with open("./obey database/last.json", "w") as f:
                    last.update({"last_id":discord_id})
                    json.dump(last, f)
                view = MemberInfo()
                await ctx.response.send_message(view=view, embed=embed)
        else:
            err=discord.Embed(description=f"❌ User is not found",color=0xcd0e0e)
            await ctx.response.send_message(embed=err)

    @app_commands.command(description="member list")
    async def memberlist(self, ctx: discord.Interaction):
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
            await ctx.response.send_message(embed=embed, view=view)

class CtxMenu(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.ctx_menu = app_commands.ContextMenu(
            name='Clan Member Info',
            callback=self.clan_info, # set the callback of the context menu to "my_cool_context_menu"
        )
        self.resend_menu = app_commands.ContextMenu(
            name='Resend Message Here',
            callback=self.resend, # set the callback of the context menu to "my_cool_context_menu"
        )
        self.client.tree.add_command(self.ctx_menu)
        self.client.tree.add_command(self.resend_menu) # add the context menu to the tree
        async def setup_hook(self) -> None:
            self.client.add_view(MemberList())

    async def clan_info(self, ctx:discord.Interaction, member: discord.Member):
        with open("./obey database/members.json", "r") as f:
            members = json.load(f)
    
        for i in members:
            if str(member.id) in members:
                discord_id = members[str(member.id)]["discord_id"]
                ingame_id = members[str(member.id)]["ingame_id"]
                valor = members[str(member.id)]["valor"]
                nick = members[str(member.id)]["nick"]
                clan_rank = members[str(member.id)]["clan_rank"]
                joined_clan = members[str(member.id)]["joined_at"]
                pic = members[str(member.id)]["pic"]
                embed = discord.Embed(description=f">>> **In-game ID:**\n {ingame_id}\n\n**Valor points:**\n{valor}\n\n**Clan Rank:**\n{clan_rank}\n\n**Joined the clan:**\n{joined_clan}\n\n**Discord ID:**\n{discord_id}", color=0x4814a3)
                embed.set_author(name=nick, icon_url=pic)
        
        with open("./obey database/last.json", "r") as f:
                    last = json.load(f)

        with open("./obey database/last.json", "w") as f:
            last.update({"last_id":member.id})
            json.dump(last, f)
        view = MemberInfo()
        await ctx.response.send_message(view=view, embed=embed)

    async def resend(self, ctx:discord.Interaction, message: discord.Message):
        await ctx.response.send_message(message.content)

async def setup(client):
    await client.add_cog(Search(client))
    await client.add_cog(CtxMenu(client))