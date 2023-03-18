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
from easy_pil import load_image_async, Editor, Font
import calendar
from obeycogs.search import MemberList
from obeycogs.help_task import TasksButtons, TopTaskDoneButton, BelowTaskDoneButton
from obeycogs.clan_info import InfoButtons

from itertools import cycle
from dateutil.relativedelta import relativedelta

class RecruitModal(discord.ui.Modal, title="Pass your info to recruit you"):
    id_here = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="1. What is your ID in game?",
        min_length=8,
        max_length=9,
        required=True,
        placeholder="Type your pg ingame id here.")

    async def on_submit(self, ctx: discord.Interaction):
            
        id = self.id_here
        OBEY = ctx.guild
        
        with open("./obey database/blacklist.json", "r") as f:
            blacklist = json.load(f)
        id = str(id)
        if id.isnumeric():
            if str(self.id_here) not in blacklist["list"]:
                OBEY = ctx.guild
                officer = get(OBEY.roles, id=985998655666401330)
                user_id = str(ctx.user.id)
                with open("./obey database/ticket_users.json", "r") as f:
                    ticket_users = json.load(f)
                    avtive = ticket_users[user_id]["active"]

                user_id = str(ctx.user.id)
                with open("./obey database/ticket_users.json", "r") as f:
                    ticket_users = json.load(f)
                    if user_id in ticket_users:
                        today = ticket_users[user_id]["today"]
                    else:
                        today = 1
                        with open("./obey database/ticket_users.json", "w") as f:
                            ticket_users.update({user_id: {"today": 0,"active": False}})
                            json.dump(ticket_users, f, indent=1)

                    with open("./obey database/ticket_counting.json", "r") as f:
                        ticket_counting = json.load(f)
                        ticket_number = ticket_counting["ticket_number"] + 1

                        if len(str(ticket_number)) == 1:
                            ticket_prefix = "000"
                        if len(str(ticket_number)) == 2:
                            ticket_prefix = "00"
                        if len(str(ticket_number)) == 3:
                            ticket_prefix = "0"
                        if len(str(ticket_number)) == 4:
                            ticket_prefix = ""

                    ticket_ebt = f"{ticket_prefix}{ticket_number}"
                    with open("./obey database/ticket_counting.json", "w") as f:
                        ticket_counting.update({"ticket_number":ticket_number})
                        json.dump(ticket_counting, f)

                    guild = ctx.guild
                    officer =get(guild.roles, id=881749441734914100)
                    category = discord.utils.get(ctx.guild.categories, name="──【 Obey 】")
                    # # ──【 Obey 】

                    obey_clan_bot = OBEY.get_member(1032359513673707591)
        
                    pfp = obey_clan_bot.display_avatar

                    log_ticket=discord.Embed(title="New Clan recruitment created",description=f"**Recruit:**\n{ctx.user.mention}\n\n**Panel**:\nApply for Obey Clan\n\n**Ticket name:**\nticket-{ticket_ebt}\n\n**Ingame ID**:\n {self.id_here}",color=0x11df3a)
                    log_ticket.set_author(name="Obey Ticketing Control", icon_url=pfp)
                    log_channel = client.get_channel(892140763792699412)
                    await log_channel.send(embed=log_ticket)
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                        ctx.user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
                        officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
                    }
                    ticket_channel = await ctx.guild.create_text_channel(name=f"ticket-{ticket_ebt}", category=category, overwrites=overwrites)

                    embed = discord.Embed(title="Answer this questions",description="[**1**] -- Do you warstart? If so then for how long?\n[**2**] -- Can you attend most raids per war?\n[**3**] -- Can you collect 5-6 incomes per day?\n[**4**] -- Can you get 1700 valor daily from clan tasks and your own?\n[**5**] -- What's your clan rank?", color=0x1e99c2)
                    embed.set_footer(text=f"IN_GAME ID: {self.id_here}")
                    await ticket_channel.send(f"Hello {ctx.user.mention}!\n\n**Welcome in the ticket, please answer the questions below and and one of our officers or leaders will respond to you as soon as this possible**\n_Remember to follow the rules during conversations with us_\n{officer.mention}", embed=embed, view=TopMenu())
                    
                    done = discord.Embed(description=f"Successfully created ticket at {ticket_channel.mention}")
                    await ctx.response.send_message(embed=done, ephemeral=True)

                    # # ticket channel id define

                    channel_id = str(ticket_channel.id)

                    # # saving user data when he/she create new ticket (today + 1 and activate ticket)

                    with open("./obey database/ticket_users.json", "r") as f:
                        ticket_users = json.load(f)
                        today = ticket_users[user_id]["today"]

                    with open("./obey database/ticket_users.json", "w") as f:
                        ticket_users.update({user_id: {"today": today + 1,"active": True}})
                        json.dump(ticket_users, f, indent=1)

                    # # saving ticket cahnnel data {cahnnel_id:user_id}

                    with open("./obey database/ticket_data.json", "r") as f:
                        ticket_data = json.load(f)

                    with open("./obey database/ticket_data.json", "w") as f:
                        ticket_data.update({channel_id:{"discord_id": user_id, "ingame_id": str(self.id_here), "num": str(ticket_ebt)}})
                        json.dump(ticket_data, f, indent=1)
            else:
                embed = discord.Embed(title="Bad spy, prepere to die!!!",color=0x1e99c2)
                await ctx.response.send_message(embed=embed, ephemeral=True)
                await asyncio.sleep(10)
                community_role = get(OBEY.roles, id=862069306463354950)
                homo = get(OBEY.roles, id=1080554474831085600)
                await ctx.user.remove_roles(community_role)
                await ctx.user.add_roles(homo)
                clan_logs = client.get_channel(1080523226586820699)
                spy_embed = discord.Embed(title="The spy was cought", description=f"**Id:**\n{self.id_here}\n\n**Spy discord name:**\n{ctx.user.mention}")
                await clan_logs.send(embed=spy_embed)
                0xd31717
                with open("./obey database/blacklist.json", "r") as f:
                    blacklist = json.load(f)
                    ingame = blacklist["list"]
                    discord_table = blacklist["discord_list"]
                with open("./obey database/blacklist.json", "w") as f:
                    discord_table.append(str(ctx.user.id))
                    blacklist.update({"list":ingame,"discord_list":discord_table})
                    json.dump(blacklist, f, indent=1)
                
        else:
            err = discord.Embed(description=f"You must pass the numbers, not text!", color=0xd31717)
            await ctx.response.send_message(embed=err, ephemeral=True)               
        
class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('?'), intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(TopMenu())
        self.add_view(CreateTicketButton())
        self.add_view(CloseConfirm())
        self.add_view(TicketingControl())
        self.add_view(MemberList())
        self.add_view(TasksButtons())
        self.add_view(TopTaskDoneButton())
        self.add_view(BelowTaskDoneButton())
        self.add_view(InfoButtons())

client = PersistentViewBot()
class TicketingControl(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)


    @discord.ui.button(custom_id="transcript_ticket", label="Transcript", style=discord.ButtonStyle.gray)
    async def transcript(self, ctx:discord.Interaction, button: discord.ui.button):
        ...

    @discord.ui.button(custom_id="open_ticket", label="Open", style=discord.ButtonStyle.green)
    async def open(self, ctx:discord.Interaction, button: discord.ui.button):

        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
        
        if admin in ctx.user.roles or officer in ctx.user.roles or ctx.user.guild_permissions.administrator:
            with open("./obey database/ticket_data.json", "r") as f:
                ticket_data = json.load(f)

            # # some user and bot data defining

            OBEY = ctx.guild
            guild = ctx.guild
            obey_clan_bot = OBEY.get_member(1032359513673707591)
            member_id = int(ticket_data[str(ctx.channel.id)]["discord_id"])
            print(member_id)
            ticket_user = OBEY.get_member(member_id)
            pfp = obey_clan_bot.display_avatar
            user = OBEY.get_member(int(member_id))
            ingame_id = ticket_data[str(ctx.channel.id)]["ingame_id"]
            num = ticket_data[str(ctx.channel.id)]["num"]
            # # permission overwrites for @everyone and ticket user
            
            officer =get(guild.roles, id=881749441734914100)

            obey_clan_bot = OBEY.get_member(1032359513673707591)
       
            pfp = obey_clan_bot.display_avatar

            log_ticket=discord.Embed(title="Clan Requirement Opened",description=f"**Recruit:**\n{user.mention}\n\n**Panel**:\nApply for Obey Clan\n\n**Ticket name:**\nticket-{num}\n\n**Ingame ID**:\n{ingame_id}",color=0x11df3a)
            log_ticket.set_author(name="Obey Ticketing Control", icon_url=pfp)
            log_channel = client.get_channel(892140763792699412)
            await log_channel.send(embed=log_ticket)
            overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    ticket_user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True),
                    officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
            }
            await ctx.channel.edit(overwrites=overwrites)

            # # channel name change to closed

            channel_name = ctx.channel.name
            ticket_number = channel_name[6:]
            new_channel_name = f"ticket-{ticket_number}"
            await ctx.channel.edit(name=new_channel_name)

            # # embed creation

            embed=discord.Embed(description=f"Ticket {ctx.channel.mention} opened by {ctx.user.mention}")
            embed.set_author(name="Obey Ticketing Control", icon_url=pfp)
            message = await ctx.channel.send(embed=embed)
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err)
            # # code end

    @discord.ui.button(custom_id="delete_ticket", label="Delete", style=discord.ButtonStyle.red)
    async def delete(self, ctx:discord.Interaction, button: discord.ui.button):

        battle_royale = client.get_emoji(1086000463775797348)
        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
        
        if admin in ctx.user.roles or officer in ctx.user.roles or ctx.user.guild_permissions.administrator:

            # # some user and bot data defining

            user_id = str(ctx.user.id)
            OBEY = ctx.guild
            obey_clan_bot = OBEY.get_member(1032359513673707591)
            pfp = obey_clan_bot.display_avatar
            
            # # embed creation

            embed=discord.Embed(description=f"Ticket will be deleted in few seconds {battle_royale}.")
            embed.set_author(name="Obey Ticketing Control", icon_url=pfp)

            # # deleting channel task with embed send too

            with open("./obey database/ticket_data.json") as f:
                ticket_data = json.load(f)
                id = ticket_data[str(ctx.channel.id)]["num"]
                ingame = ticket_data[str(ctx.channel.id)]["ingame_id"]
                discord_id = ticket_data[str(ctx.channel.id)]["discord_id"]
                user = OBEY.get_member(int(discord_id))

            await ctx.channel.send(embed=embed)
            await asyncio.sleep(10)
            await ctx.channel.delete()

            log_ticket=discord.Embed(title="Clan recruitment deleted",description=f"**Recruit:**\n{user.mention}\n\n**Panel**:\nApply for Obey Clan\n\n**Ticket Name:**\nticket-{id}\n\n**Ingame ID:**\n{ingame}",color=0xdf1111)
            log_ticket.set_author(name="Obey Ticketing Control", icon_url=pfp)
            log_channel = client.get_channel(892140763792699412)
            await log_channel.send(embed=log_ticket)

            # # setting user ticket active to false so member can create another ticket (max 2 per day)

            with open("./obey database/ticket_users.json", "r") as f:
                ticket_users = json.load(f)
                today = ticket_users[discord_id]["today"]
            
            with open("./obey database/ticket_users.json", "w") as f:
                ticket_users.update({user_id: {"today": today,"active": False}})
                json.dump(ticket_users, f, indent=1)

            # # deleting ticket channel data from ticket_data

            with open("./obey database/ticket_data.json", "r") as f:
                ticket_data = json.load(f)
                ticket_data.pop(str(ctx.channel.id))

            with open("./obey database/ticket_data.json", "w") as f:
                json.dump(ticket_data, f, indent=1)
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err)    
            # # code end

class CloseConfirm(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(custom_id="close_confirm", label="Close", style=discord.ButtonStyle.gray)
    async def close(self, ctx:discord.Interaction, button: discord.ui.button):
        
        with open("./obey database/ticket_data.json", "r") as f:
            ticket_data = json.load(f)

        # # some user and bot data defining

        OBEY = ctx.guild
        guild = ctx.guild
        obey_clan_bot = OBEY.get_member(1032359513673707591)
        member_id = int(ticket_data[str(ctx.channel.id)]["discord_id"])
        print(member_id)
        ticket_user = OBEY.get_member(member_id)
        pfp = obey_clan_bot.display_avatar
        
        # # permission overwrites for @everyone and ticket user

        officer = get(guild.roles, id=881749441734914100) 
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ticket_user: discord.PermissionOverwrite(view_channel = True, send_messages = False, attach_files=False, embed_links = False),
            officer: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files=True, embed_links = True)
            }
        await ctx.channel.edit(overwrites=overwrites)

        # # channel name change to closed

        channel_name = ctx.channel.name
        ticket_number = channel_name[6:]
        new_channel_name = f"closed-{ticket_number}"
        await ctx.channel.edit(name=new_channel_name)

        # # embed creation

        embed=discord.Embed(description=f"Ticket {ctx.channel.mention} closed by {ctx.user.mention}")
        embed.set_author(name="Obey Ticketing Control", icon_url=pfp)
        message = await ctx.channel.send(embed=embed, view=TicketingControl())

        # # code end

class TopMenu(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(custom_id="close_ticket", label="Close", style=discord.ButtonStyle.gray, emoji="🔒")
    async def close(self, ctx:discord.Interaction, button: discord.ui.button):

            OBEY = ctx.guild
            obey_clan_bot = OBEY.get_member(1032359513673707591)
            pfp = obey_clan_bot.display_avatar

            embed=discord.Embed(description="Are You sure to close this ticket?")
            embed.set_author(name="Obey Ticketing Control", icon_url=pfp)
            await ctx.response.send_message(embed=embed, view=CloseConfirm(), ephemeral=True)

    @discord.ui.button(custom_id="add_member", label="Add member", style=discord.ButtonStyle.green)
    async def add_member(self, ctx:discord.Interaction, button: discord.ui.button):

        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
        
        if admin in ctx.user.roles or officer in ctx.user.roles:
            channel_id = str(ctx.channel.id)

            time_now = datetime.datetime.now()
            time_after = str(time_now + datetime.timedelta(minutes=1))

            with open("./obey database/ticket_data.json", "r") as f:
                ticket_data = json.load(f)
                id = ticket_data[channel_id]["ingame_id"]
                discord_id = int(ticket_data[channel_id]["discord_id"])
            OBEY = ctx.guild
            user = OBEY.get_member(discord_id)
            nick = str(user.name)
            new_name = f"{nick} | {id}"
            await user.edit(nick=new_name)
            clan_role = get(OBEY.roles, id=881330782185074718)
            await user.add_roles(clan_role)
            with open("./obey database/members.json", "r") as f:
                members = json.load(f)
            with open("./obey database/members.json", "w") as f:
                members.update({str(discord_id): {
                    "ingame_id": str(id),
                    "valor": "0",
                    "clan_rank": "Clan Member",
                    "nick": nick,
                    "discord_id": str(discord_id),
                    "joined_at": time_after[0:16],
                    "pic": str(user.display_avatar)
                }})
                json.dump(members, f, indent=1)
            embed=discord.Embed(description=f"✅ Added {user.name} to clan!",color=0x1f9336)
            await ctx.response.send_message(embed=embed)
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err, ephemeral=True)   

class CreateTicketButton(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(custom_id="create_ticket", label="Create Ticket", style=discord.ButtonStyle.gray)
    async def create_ticket(self, ctx:discord.Interaction, button: discord.ui.button):
        
        user_id = str(ctx.user.id)
        with open("./obey database/ticket_users.json", "r") as f:
            ticket_users = json.load(f)
            if user_id in ticket_users:
                today = ticket_users[user_id]["today"]
            else:
                today = 1
                with open("./obey database/ticket_users.json", "w") as f:
                    ticket_users.update({user_id: {"today": 0,"active": False}})
                    json.dump(ticket_users, f, indent=1)

        with open("./obey database/ticket_users.json", "r") as f:
                ticket_users = json.load(f)
                active = ticket_users[user_id]["active"]

        if active==False:
            if today<2:
                await ctx.response.send_modal(RecruitModal())
            else:
                err = discord.Embed(title="Ticket Error",description=f"You can only make 2 tickets per day!")
                await ctx.response.send_message(embed=err, ephemeral=True)
        else:
            err = discord.Embed(title="Ticket Error",description=f"You had opened ticket already!")
            await ctx.response.send_message(embed=err, ephemeral=True)

@client.tree.command()
async def create_ticket(ctx: discord.Interaction) -> None:
        
        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
        
        if admin in ctx.user.roles or officer in ctx.user.roles or ctx.user.guild_permissions.administrator:
            OBEY = ctx.guild
            obey_clan_bot = OBEY.get_member(1032359513673707591)
            pfp = obey_clan_bot.display_avatar
            requirements = discord.Embed(title="__の乃乇ﾘ   Requirements__", description="[**1**] -- Can you **Warstart?** If so how long?\n[**2**] -- How many raids can you attend per war?\n[**3**] -- **Frequently check Discord**.\n[**4**] -- **Collect 5-6 incomes per day**.\n[**5**] -- **Get 1800 valor daily from clan tasks and your own?**\n**[**6**] -- Can you reach 18.000 valor points before war end?**\n**[**7**] -- Lt. Colonel + \n[**8**] -- Level 65**\n\n**__Before creating a ticket__**\n**Do NOT create a ticket if you cannot meet the requirements above**.", color=0xd80e4a)
            requirements.set_thumbnail(url="https://images-ext-1.discordapp.net/external/v1P69Mafmm_8sHrUJ_KTyU7PCFTm9b5yPY_dpVbai8E/https/cdn-longterm.mee6.xyz/plugins/embeds/images/706466887734919180/4ffa20e2d9a9192cbfe4978059c291a8ab870998c725dd5949a879d8abc2c3c8.png")
            requirements.set_image(url="https://i.imgur.com/TswvMUj.png")
            
            ticket_embed = discord.Embed(description="""**Click the** **__"Create Ticket"__** **button below and send your id to discord form, then our ticket system will create ticket for you in which you must answer the questions.**(**__when button doesn't working - click it again__**)""", color=0xd80e4a)
            ticket_embed.set_author(name=obey_clan_bot.name, icon_url=pfp)
            ticket_embed.set_footer(text="Obey Ticketing System | {}".format(ctx.created_at.strftime("%H:%M")))

            view = CreateTicketButton()
            await ctx.response.send_message("Test Ticket Message Below")
            await ctx.channel.send(embed=requirements)
            await ctx.channel.send(embed=ticket_embed, view=view)
        else:
            err=discord.Embed(description=f"❌ {ctx.user} you can't use that!",color=0xcd0e0e)
            await ctx.response.send_message(embed=err)

@client.event
async def on_ready():
    for i in os.listdir("./obeycogs"):
                if i.endswith(".py"):
                    await client.load_extension(f"obeycogs.{i[:-3]}")
                    print(f"Pomyślnie załadowano cog: {i}")
    channel = client.get_channel(1025734128303345734)
    synced = await client.tree.sync()
    await channel.send("Działam")

@client.event
async def on_member_join(member):

    discord_id = str(member.id)

    with open("./obey database/blacklist.json", "r") as f:
        blacklist = json.load(f)
        discord_table = blacklist["discord_list"]

    if discord_id in discord_table:
        guild = client.get_guild(706466887734919180)
        homo = get(guild.roles, id=1080554474831085600)
        await member.add_roles(homo) 



if __name__ == "__main__":
    with open("token.json", "r") as toks:
        token = json.load(toks)
        TOKEN = token["token"]
    client.run(TOKEN)