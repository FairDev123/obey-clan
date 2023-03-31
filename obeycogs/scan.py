import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands
import json

class ScanCommand(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @app_commands.command(description="search for id in the blacklist from clan member name")
    async def scan(self, ctx: discord.Interaction):

        with open("./obey database/blacklist.json", "r") as f:
            blacklist = json.load(f)

        guild = ctx.guild

        clan_member = get(guild.roles, id=881330782185074718)
        
        clear_members = []
        sus_members = []
        trusted_team = []

        for i in clan_member.members:

            member_id = str(i.nick)[-9:]
            print(member_id.strip())
            admin = discord.utils.get(ctx.user.roles, name="Administrator")
            officer =get(guild.roles, id=881749441734914100)
        
            if admin in i.roles or officer in i.roles:
                trusted_team.append(f"{str(i.mention)}")
            else:
                if member_id.strip() in blacklist["list"]:
                    sus_members.append(f"{str(i.mention)}")
                else:
                    clear_members.append(f"{str(i.mention)}")

            clear = " ".join(member_name for member_name in clear_members)
            sus = " ".join(member_name for member_name in sus_members)
            trusted = " ".join(member_name for member_name in trusted_team)

        clear_len = len(clear_members)
        sus_len = len(sus_members)
        embed = discord.Embed(title="Spy Scan results:", description=f"❤️ **Trusted team**:\n{trusted}\n\n**✅ List of clear clan members**:\n{clear}\n{clear_len} members!\n\n**❌ List of suspects:**\n{sus}\n{sus_len} members!", color=0xd80e4a)
        await ctx.response.send_message(embed=embed)


async def setup(client):
    await client.add_cog(ScanCommand(client))
