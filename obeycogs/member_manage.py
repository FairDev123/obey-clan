import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands
import json
import datetime
import mysql.connector
from groups.search import MembersListButtons

async def add_role(var, ctx):

    with open("./obey database/temp_user.json", "r") as f:
        temp_user = json.load(f)

    with open("./obey database/blacklist.json", "r") as f:
        blacklist = json.load(f)
        blacklist_ds = blacklist["discord_list"]
        blacklist_pg = blacklist["list"]

    guild = ctx.guild
    member = guild.get_member(int(temp_user[str(ctx.user.id)]["user_id"]))
    
    if var=="Not in Clan Rn":
        
        clan_member_role =get(guild.roles, id=881330782185074718)
        not_in_clan_rn =get(guild.roles, id=988039468013473802)

        await member.add_roles(not_in_clan_rn)
        await member.remove_roles(clan_member_role)
        embed = discord.Embed(title=f"Saccessfully {not_in_clan_rn.mention} was added")
        await ctx.response.send_message(embed=embed, ephemeral=True)

    if var=="Ally":
        
        ally =get(guild.roles, id=989171283348574268)

        await member.add_roles(ally)
        embed = discord.Embed(title=f"Saccessfully {ally.mention} was added")
        await ctx.response.send_message(embed=embed, ephemeral=True)

    if var=="Ally Clan Leader":
        
        ally_leader =get(guild.roles, id=1087894288601464832)

        await member.add_roles(ally_leader)
        embed = discord.Embed(title=f"Saccessfully {ally_leader.mention} was added")
        await ctx.response.send_message(embed=embed, ephemeral=True)

    if var=="Helper":
        
        helper =get(guild.roles, id=980100979171151922)

        await member.add_roles(helper)
        embed = discord.Embed(title=f"Saccessfully {helper.mention} was added")
        await ctx.response.send_message(embed=embed, ephemeral=True)

    if var=="Spy":
        
        spy =get(guild.roles, id=1087364654017298454)

        helper =get(guild.roles, id=980100979171151922)
        ally_leader =get(guild.roles, id=1087894288601464832)
        ally =get(guild.roles, id=989171283348574268)
        clan_member_role =get(guild.roles, id=881330782185074718)
        not_in_clan_rn =get(guild.roles, id=988039468013473802)
        community =get(guild.roles, id=862069306463354950)

        await member.add_roles(spy)
        
        await member.remove_roles(helper)
        await member.remove_roles(ally_leader)
        await member.remove_roles(ally)
        await member.remove_roles(clan_member_role)
        await member.remove_roles(not_in_clan_rn)
        await member.remove_roles(community)

        blacklist_ds.append(str(member.id))
        with open("./obey database/blacklist.json", "w") as f:
            blacklist.update({"list":blacklist_pg, "discord_list":blacklist_ds})
            json.dump(blacklist, f, indent=1)

        embed = discord.Embed(title=f"Saccessfully {spy.mention} was added")
        await ctx.response.send_message(embed=embed, ephemeral=True)
        
async def add_clanmate(ctx, clanmate_id):
    with open("./obey database/temp_user.json", "r") as f:
        temp_user = json.load(f)
    with open("./obey database/blacklist.json", "r") as f:
        blacklist  = json.load(f)
        blacklist_pg = blacklist["list"]
        guild = ctx.guild
        clan_member_role =get(guild.roles, id=881330782185074718)

        member = guild.get_member(int(temp_user[str(ctx.user.id)]["user_id"]))

    if str(clanmate_id) not in blacklist_pg:

        with open("./obey database/members.json", "r") as f:
            members = json.load(f)

        time_now = datetime.datetime.now()
        time_after = str(time_now - datetime.timedelta(minutes=1))
        members.update({str(member.id):{
            "ingame_id": str(clanmate_id),
            "valor": "0",
            "clan_rank": "Clan Member",
            "nick": str(member.name),
            "discord_id": str(member.id),
            "joined_at": time_after[0:16],
            "pic": str(member.display_avatar)
        }})

        with open("./obey database/members.json", "w") as f:
            json.dump(members, f, indent=1)

        member_name = f"{member.name} | {clanmate_id}"
        await member.edit(nick=member_name)

        await member.add_roles(clan_member_role)

        embed = discord.Embed(title=f"Saccessfully new Clan Member was added to the clan!")
        await ctx.response.send_message(embed=embed, ephemeral=True)
    else:
        embed=discord.Embed(title="Spy detected!", description=f"{member.mention} is in the blacklist!")
        await ctx.response.send_message(embed=embed, ephemeral=True)


class AddModal(discord.ui.Modal, title="Pass recruit id"):
    id_here = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="1. What is ID of recruit?",
        min_length=8,
        max_length=9,
        required=True,
        placeholder="Type recruit pg ingame id here.")

    async def on_submit(self, ctx: discord.Interaction):
        
        await add_clanmate(ctx, self.id_here)

class ClanRoles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(custom_id="add_clan_member", label="Clan member", style=discord.ButtonStyle.green)
    async def clan_member(self, ctx:discord.Interaction, button: discord.ui.button):
        await ctx.response.send_modal(AddModal())

    @discord.ui.button(custom_id="add_not_in_clan_rn", label="Not In Clan Rn", style=discord.ButtonStyle.gray)
    async def not_in_clan(self, ctx:discord.Interaction, button: discord.ui.button):
        var = "Not in Clan Rn"
        await add_role(var, ctx)

    @discord.ui.button(custom_id="add_ally", label="Ally", style=discord.ButtonStyle.gray)
    async def ally(self, ctx:discord.Interaction, button: discord.ui.button):
        var = "Ally"
        await add_role(var, ctx)

    @discord.ui.button(custom_id="add_ally_leader", label="Ally Clan Leader", style=discord.ButtonStyle.gray)
    async def ally_leader(self, ctx:discord.Interaction, button: discord.ui.button):
        var = "Ally Clan Leader"
        await add_role(var, ctx)

    @discord.ui.button(custom_id="add_helper", label="Helper", style=discord.ButtonStyle.gray)
    async def helper(self, ctx:discord.Interaction, button: discord.ui.button):
        var = "Helper"
        await add_role(var, ctx)

    @discord.ui.button(custom_id="add_spy", label="Spy", style=discord.ButtonStyle.red)
    async def spy(self, ctx:discord.Interaction, button: discord.ui.button):
        var = "Spy"
        await add_role(var, ctx)

class MemberButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(custom_id="add_clan_roles1", label="Add Clan Roles", style=discord.ButtonStyle.green)
    async def add_clan_roles(self, ctx:discord.Interaction, button: discord.ui.button):
        guild = ctx.guild
        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer =get(guild.roles, id=881749441734914100)
        
        if admin in ctx.user.roles or officer in ctx.user.roles or ctx.user.guild_permissions.administrator:
            await ctx.response.send_message("test", view=ClanRoles(), ephemeral=True)

class ClanmateButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(custom_id="add_clan_roles2", label="Add Clan Roles", style=discord.ButtonStyle.green)
    async def add_clan_roles(self, ctx:discord.Interaction, button: discord.ui.button):
        guild = ctx.guild
        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer =get(guild.roles, id=881749441734914100)
        
        if admin in ctx.user.roles or officer in ctx.user.roles or ctx.user.guild_permissions.administrator:
            await ctx.response.send_message("test", view=ClanRoles(), ephemeral=True)

    @discord.ui.button(custom_id="clanmate_info", label="Clanmate Info", style=discord.ButtonStyle.green)
    async def clanmate_info(self, ctx:discord.Interaction, button: discord.ui.button):

        guild = ctx.guild
        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer =get(guild.roles, id=881749441734914100)
        
        if admin in ctx.user.roles or officer in ctx.user.roles or ctx.user.guild_permissions.administrator:
            
            await ctx.response.defer(thinking=True, ephemeral=True)

            with open("db_con_info.json", "r") as f:
                db_con = json.load(f)
                host = db_con["host"]
                user = "admin"
                password = db_con["pass"]
                port = db_con["port"]
            
            db = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            port=port,
            database="Obey Clan")

            with open("./obey database/user_query.json", "r") as f:
                user_query = json.load(f)
                discord_id = user_query[str(ctx.user.id)]["user_id"]

            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM members WHERE discord_id={discord_id}")

            discord_ids, discord_names, pg_ids, pg_names, clan_ranks, valors = [],[],[],[],[],[]
            data = {}

            for col_id, disocrd_id, discord_name, pg_id, pg_name, clan_rank, valor in cursor:
                discord_ids.append(disocrd_id)
                discord_names.append(discord_name)
                pg_ids.append(pg_id)
                pg_names.append(pg_name)
                clan_ranks.append(clan_rank)
                valors.append(valor)
                break
            
            data.update({"discord_ids":discord_ids,"discord_names":discord_names,"pg_ids":pg_ids,"pg_names":pg_names,"clan_ranks":clan_ranks,"valors":valors})

            member = ctx.guild.get_member(discord_ids[0])

            user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
            user_info.set_thumbnail(url=member.display_avatar)
            user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
            user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            await ctx.followup.send(embed=user_info, ephemeral=True)

class AddingToClan(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @app_commands.command(description="editing member")
    async def edit(self, ctx: discord.Interaction, member: discord.Member = None):

        guild = ctx.guild
        admin = discord.utils.get(ctx.user.roles, name="Administrator")
        officer =get(guild.roles, id=881749441734914100)
        
        if admin in ctx.user.roles or officer in ctx.user.roles or ctx.user.guild_permissions.administrator:

            member_id = member.id
            with open("./obey database/members.json", "r") as f:
                members = json.load(f)

            with open("db_con_info.json", "r") as f:
                db_con = json.load(f)
                host = db_con["host"]
                user = "admin"
                password = db_con["pass"]
                port = db_con["port"]
                
            db = mysql.connector.connect(
                host=host,
                user=user,
                passwd=password,
                port=port,
                database="Obey Clan")

            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM members")

            discord_ids, discord_names, pg_ids, pg_names, clan_ranks, valors = [],[],[],[],[],[]
            data = {}

            for col_id, disocrd_id, discord_name, pg_id, pg_name, clan_rank, valor in cursor:
                    discord_ids.append(disocrd_id)
                    discord_names.append(discord_name)
                    pg_ids.append(pg_id)
                    pg_names.append(pg_name)
                    clan_ranks.append(clan_rank)
                    valors.append(valor)
            
            data.update({"discord_ids":discord_ids,"discord_names":discord_names,"pg_ids":pg_ids,"pg_names":pg_names,"clan_ranks":clan_ranks,"valors":valors})
            print(data)
            
            user_roles = " ".join(role.mention for role in member.roles)
            user_perms = " ".join(str(permission.count) for permission in member.guild_permissions)

            edit_embed = discord.Embed(title="Info about this member", description=f"{member.mention}\n**User Roles:**\n{user_roles}\n\n**Joined at:**\n{member.joined_at}\n\n**Discord ID:**\n{member.id}",color=0xd80e4a)
            edit_embed.set_author(icon_url=member.display_avatar, name=member.display_name)
            edit_embed.set_thumbnail(url=member.display_avatar)

            if int(member_id) in data["discord_ids"]:
                await ctx.response.send_message(embed=edit_embed, view=ClanmateButtons())
            else:
                await ctx.response.send_message(embed=edit_embed, view=MemberButtons())

            with open("./obey database/user_query.json", "r") as f:
                temp_user = json.load(f)
                user_id = str(member_id)
            with open("./obey database/user_query.json", "w") as f:
                temp_user.update({str(ctx.user.id):{"user_id":user_id,"data":data}})
                json.dump(temp_user, f)
            
async def setup(client):
    await client.add_cog(AddingToClan(client))
