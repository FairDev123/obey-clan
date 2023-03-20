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
import asyncio
import time as tm
import json
import os

class GuideButtons(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(custom_id="guide-1", label="1", style=discord.ButtonStyle.gray)
    async def guide_1(self, ctx:discord.Interaction, button: discord.ui.button):
        guide_1 = discord.Embed(title=f"How to add member to the bot database?", description="**Command example:**\n\n**/rawjoin member: FairShooter123 id:123456789 clan_role: Clan Member**\n\nBasically **__member__** is argument which can be passed by discord id but you can still use tag, **__id argument__** is a keyword which must been passed here because later you want search for user by id from the game, and last argument its a **__clan role__** which you can choose from the list when you execute this keyword\n\n**So that command ascribes __ingame id__ to the user from discord which is helpful later when you need search for low valor user**", color=0xd80e4a)
        await ctx.response.send_message(embed=guide_1)

class GuideBook(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    async def guide_book(self, ctx: discord.Interaction):
        clan_member = discord.utils.get(ctx.user.roles, name="Clan Member")
        officer = discord.utils.get(ctx.user.roles, name="Clan Officer")
        admin = discord.utils.get(ctx.user.roles, name="Administrator")

        if admin in ctx.user.roles or officer in ctx.user.roles or clan_member in ctx.user.roles:
            task_completion = self.client.get_channel(1081235077654118450)
            task_help = self.client.get_channel(1085984350589440170)
            guide_book = discord.Embed(title=f"[📚] Guide book for Obey Staff", description=f"Below are the questions for each command, click on the corresponding button to view the guide book of this command\n\n**1** - How to add member to the bot database?\n\n**2** - How to add and remove member from blacklist?\n\n**3** - How to use Obey Ticketing System?\n\n**4** - How {task_completion.mention} channel work?\n\n**5** - How to use {task_help.mention} channel?\n\n**6** - How to search in the clan members database?", color=0xd80e4a)
            await ctx.response.send_message(embed=guide_book, view=GuideButtons())

async def setup(client):
    await client.add_cog(GuideBook(client))
