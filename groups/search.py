import discord
from discord import app_commands
import mysql.connector
import json
from discord.app_commands import Choice

class MembersListButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(custom_id="pagination_search_previos", label="Previous", style=discord.ButtonStyle.green, emoji="⬅️")
    async def previous_member_search(self, ctx:discord.Interaction, button: discord.ui.button):

        with open("./obey database/user_query.json", "r") as f:
            user_query = json.load(f)
            data = user_query[str(ctx.user.id)]["data"]

            page = user_query[str(ctx.user.id)]["page"]
            discord_ids = data["discord_ids"]
            discord_names = data["discord_names"]
            pg_ids = data["pg_ids"]
            pg_names = data["pg_names"]
            clan_ranks = data["clan_ranks"]
            valors = data["valors"]

        if page != 0:
            page = page - 1
        else:
            page = len(discord_ids) - 1
        
        discord_id = discord_ids[page]
        discord_name = discord_names[page]
        pg_id = pg_ids[page]
        pg_name = pg_names[page]
        clan_rank = clan_ranks[page]
        valor = valors[page]

        member = ctx.guild.get_member(discord_id)

        user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
        user_info.set_thumbnail(url=member.display_avatar)
        user_info.set_footer(text=f"Page {page + 1}/{len(discord_ids)}")
        user_info.set_author(name=discord_name,icon_url=member.display_avatar)
        await ctx.response.edit_message(embed=user_info, view=MembersListButtons())

        with open("./obey database/user_query.json", "w") as f:
            user_query.update({str(ctx.user.id):{"data":data,"page": page}})
            json.dump(user_query, f)

    @discord.ui.button(custom_id="pagination_search_next", label="Next", style=discord.ButtonStyle.green, emoji="➡️")
    async def next_member_search(self, ctx:discord.Interaction, button: discord.ui.button):

        with open("./obey database/user_query.json", "r") as f:
            user_query = json.load(f)
            data = user_query[str(ctx.user.id)]["data"]

            page = user_query[str(ctx.user.id)]["page"]
            discord_ids = data["discord_ids"]
            discord_names = data["discord_names"]
            pg_ids = data["pg_ids"]
            pg_names = data["pg_names"]
            clan_ranks = data["clan_ranks"]
            valors = data["valors"]
        
        if page != (len(discord_ids) - 1):
            page = page + 1
        else:
            page = 0
        
        discord_id = discord_ids[page]
        discord_name = discord_names[page]
        pg_id = pg_ids[page]
        pg_name = pg_names[page]
        clan_rank = clan_ranks[page]
        valor = valors[page]

        member = ctx.guild.get_member(discord_id)

        user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
        user_info.set_thumbnail(url=member.display_avatar)
        user_info.set_footer(text=f"Page {page + 1}/{len(discord_ids)}")
        user_info.set_author(name=discord_name,icon_url=member.display_avatar)
        await ctx.response.edit_message(embed=user_info, view=MembersListButtons())

        with open("./obey database/user_query.json", "w") as f:
            user_query.update({str(ctx.user.id):{"data":data,"page": page}})
            json.dump(user_query, f)

class MojaGrupa(app_commands.Group):
    @app_commands.command(description="Search member by member id (require discord tag - mention)")
    async def member(self, ctx: discord.Interaction, member_tag:discord.Member=None):

        await ctx.response.defer()

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
            cursor.execute(f"SELECT * FROM members WHERE discord_id={member_tag.id}")

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

            if len(discord_ids) > 0:
                discord_id = discord_ids[0]
                discord_name = discord_names[0]
                pg_id = pg_ids[0]
                pg_name = pg_names[0]
                clan_rank = clan_ranks[0]
                valor = valors[0]

                with open("./obey database/user_query.json", "r") as f:
                    user_query = json.load(f)

                with open("./obey database/user_query.json", "w") as f:
                    user_query.update({str(ctx.user.id):{"data":data,"page":0}})
                    json.dump(user_query, f, indent=1)

                member = ctx.guild.get_member(discord_id)

                user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
                user_info.set_thumbnail(url=member.display_avatar)
                user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
                user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            if len(data["discord_ids"]) > 1:
                await ctx.followup.send(embed=user_info, view=MembersListButtons())
            elif len(data["discord_ids"]) == 1:
                await ctx.followup.send(embed=user_info)
            else:
                await ctx.followup.send("Nothing found!")

    @app_commands.command(description="Search member by discord_id(search by member does the sam thing)")
    async def discord_id(self, ctx: discord.Interaction, member_id:int=0):
        await ctx.response.defer()

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
            cursor.execute(f"SELECT * FROM members WHERE discord_id={ctx.user.id}")

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

            if len(discord_ids) > 0:
                discord_id = discord_ids[0]
                discord_name = discord_names[0]
                pg_id = pg_ids[0]
                pg_name = pg_names[0]
                clan_rank = clan_ranks[0]
                valor = valors[0]

                with open("./obey database/user_query.json", "r") as f:
                    user_query = json.load(f)

                with open("./obey database/user_query.json", "w") as f:
                    user_query.update({str(ctx.user.id):{"data":data,"page":0}})
                    json.dump(user_query, f, indent=1)

                member = ctx.guild.get_member(discord_id)

                user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
                user_info.set_thumbnail(url=member.display_avatar)
                user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
                user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            if len(data["discord_ids"]) > 1:
                await ctx.followup.send(embed=user_info, view=MembersListButtons())
            elif len(data["discord_ids"]) == 1:
                await ctx.followup.send(embed=user_info)
            else:
                await ctx.followup.send("Nothing found!")

    @app_commands.command(description="Search member by his name, id exist bot return all members with that name")
    async def discord_name(self, ctx: discord.Interaction, discord_name:str=None):
        await ctx.response.defer()

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
            cursor.execute(f"SELECT * FROM members WHERE discord_id={ctx.user.id}")

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

            if len(discord_ids) > 0:
                discord_id = discord_ids[0]
                discord_name = discord_names[0]
                pg_id = pg_ids[0]
                pg_name = pg_names[0]
                clan_rank = clan_ranks[0]
                valor = valors[0]

                with open("./obey database/user_query.json", "r") as f:
                    user_query = json.load(f)

                with open("./obey database/user_query.json", "w") as f:
                    user_query.update({str(ctx.user.id):{"data":data,"page":0}})
                    json.dump(user_query, f, indent=1)

                member = ctx.guild.get_member(discord_id)

                user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
                user_info.set_thumbnail(url=member.display_avatar)
                user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
                user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            if len(data["discord_ids"]) > 1:
                await ctx.followup.send(embed=user_info, view=MembersListButtons())
            elif len(data["discord_ids"]) == 1:
                await ctx.followup.send(embed=user_info)
            else:
                await ctx.followup.send("Nothing found!")
    @app_commands.command(description="Search member by discord_id(search by member does the sam thing)")
    async def discord_id(self, ctx: discord.Interaction, member_id:str):
        await ctx.response.defer()

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
            cursor.execute(f"SELECT * FROM members WHERE discord_id={member_id}")

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

            if len(discord_ids) > 0:
                discord_id = discord_ids[0]
                discord_name = discord_names[0]
                pg_id = pg_ids[0]
                pg_name = pg_names[0]
                clan_rank = clan_ranks[0]
                valor = valors[0]

                with open("./obey database/user_query.json", "r") as f:
                    user_query = json.load(f)

                with open("./obey database/user_query.json", "w") as f:
                    user_query.update({str(ctx.user.id):{"data":data,"page":0}})
                    json.dump(user_query, f, indent=1)

                member = ctx.guild.get_member(discord_id)

                user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
                user_info.set_thumbnail(url=member.display_avatar)
                user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
                user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            if len(data["discord_ids"]) > 1:
                await ctx.followup.send(embed=user_info, view=MembersListButtons())
            elif len(data["discord_ids"]) == 1:
                await ctx.followup.send(embed=user_info)
            else:
                await ctx.followup.send("Nothing found!")

    @app_commands.command(description="Search member by his name, id exist bot return all members with that name")
    async def discord_name(self, ctx: discord.Interaction, discord_name:str):
        await ctx.response.defer()

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
            cursor.execute(f"SELECT * FROM members WHERE discord_id={discord_name}")

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

            if len(discord_ids) > 0:
                discord_id = discord_ids[0]
                discord_name = discord_names[0]
                pg_id = pg_ids[0]
                pg_name = pg_names[0]
                clan_rank = clan_ranks[0]
                valor = valors[0]

                with open("./obey database/user_query.json", "r") as f:
                    user_query = json.load(f)

                with open("./obey database/user_query.json", "w") as f:
                    user_query.update({str(ctx.user.id):{"data":data,"page":0}})
                    json.dump(user_query, f, indent=1)

                member = ctx.guild.get_member(discord_id)

                user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
                user_info.set_thumbnail(url=member.display_avatar)
                user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
                user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            if len(data["discord_ids"]) > 1:
                await ctx.followup.send(embed=user_info, view=MembersListButtons())
            elif len(data["discord_ids"]) == 1:
                await ctx.followup.send(embed=user_info)
            else:
                await ctx.followup.send("Nothing found!")
    @app_commands.command(description="Search member by discord_id(search by member does the sam thing)")
    async def pg_id(self, ctx: discord.Interaction, pg_id:int):
        await ctx.response.defer()

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
            cursor.execute(f"SELECT * FROM members WHERE pg_id={pg_id}")

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

            if len(discord_ids) > 0:
                discord_id = discord_ids[0]
                discord_name = discord_names[0]
                pg_id = pg_ids[0]
                pg_name = pg_names[0]
                clan_rank = clan_ranks[0]
                valor = valors[0]

                with open("./obey database/user_query.json", "r") as f:
                    user_query = json.load(f)

                with open("./obey database/user_query.json", "w") as f:
                    user_query.update({str(ctx.user.id):{"data":data,"page":0}})
                    json.dump(user_query, f, indent=1)

                member = ctx.guild.get_member(discord_id)

                user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
                user_info.set_thumbnail(url=member.display_avatar)
                user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
                user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            if len(data["discord_ids"]) > 1:
                await ctx.followup.send(embed=user_info, view=MembersListButtons())
            elif len(data["discord_ids"]) == 1:
                await ctx.followup.send(embed=user_info)
            else:
                await ctx.followup.send("Nothing found!")

    @app_commands.command(description="Search member by his name, id exist bot return all members with that name")
    async def pg_name(self, ctx: discord.Interaction, pg_name:str):
        await ctx.response.defer()

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
            cursor.execute(f"SELECT * FROM members WHERE pg_name='{pg_name}'")

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

            if len(discord_ids) > 0:
                discord_id = discord_ids[0]
                discord_name = discord_names[0]
                pg_id = pg_ids[0]
                pg_name = pg_names[0]
                clan_rank = clan_ranks[0]
                valor = valors[0]

                with open("./obey database/user_query.json", "r") as f:
                    user_query = json.load(f)

                with open("./obey database/user_query.json", "w") as f:
                    user_query.update({str(ctx.user.id):{"data":data,"page":0}})
                    json.dump(user_query, f, indent=1)

                member = ctx.guild.get_member(discord_id)

                user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
                user_info.set_thumbnail(url=member.display_avatar)
                user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
                user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            if len(data["discord_ids"]) > 1:
                await ctx.followup.send(embed=user_info, view=MembersListButtons())
            elif len(data["discord_ids"]) == 1:
                await ctx.followup.send(embed=user_info)
            else:
                await ctx.followup.send("Nothing found!")
    
    @app_commands.command(description="Search member by valor(you can make statements like income>9000), return list")
    async def valor(self, ctx: discord.Interaction, valor:str=None):
        await ctx.response.defer()

        if ">" in valor:
            statement = ">"
            if "=" in valor:
                statement = ">="
        elif "<" in valor:
            statement = "<"
            if "=" in valor:
                statement = "<="
        elif "=" in valor and ">" not in valor and "<" not in valor:
            statement="="
        else:
            statement = "None"
        
        num_list = ""
        for i in valor:
            if i.isnumeric():
                num_list = num_list + i
        
        valor = num_list

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

            if statement == "None":
                cursor.execute(f"SELECT * FROM members WHERE valors={valor}")
            else:
                cursor.execute(f"SELECT * FROM members WHERE valors{statement}{valor}")

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

            if len(discord_ids) > 0:
                discord_id = discord_ids[0]
                discord_name = discord_names[0]
                pg_id = pg_ids[0]
                pg_name = pg_names[0]
                clan_rank = clan_ranks[0]
                valor = valors[0]

                with open("./obey database/user_query.json", "r") as f:
                    user_query = json.load(f)

                with open("./obey database/user_query.json", "w") as f:
                    user_query.update({str(ctx.user.id):{"data":data,"page":0}})
                    json.dump(user_query, f, indent=1)

                member = ctx.guild.get_member(discord_id)

                user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
                user_info.set_thumbnail(url=member.display_avatar)
                user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
                user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            if len(data["discord_ids"]) > 1:
                await ctx.followup.send(embed=user_info, view=MembersListButtons())
            elif len(data["discord_ids"]) == 1:
                await ctx.followup.send(embed=user_info)
            else:
                await ctx.followup.send("Nothing found!")

    @app_commands.command(description="Search member by his name, id exist bot return all members with that name")
    @app_commands.choices(clan_rank=[
    Choice(name="Clan Member", value="Clan Member"),
    Choice(name="Clan Leader", value="Clan Leader"),
    Choice(name="Clan Co-Leader", value="Clan Co-Leader"),
    Choice(name="Clan Officer", value="Clan Officer"),
    Choice(name="Ally Clan Leader", value="Ally Clan Leader"),
    Choice(name="Ally", value="Ally"),
    Choice(name="Helper", value="Helper")
])
    async def clan_rank(self, ctx: discord.Interaction, clan_rank:str="Clan Member"):
        await ctx.response.defer()

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
            cursor.execute(f"SELECT * FROM members WHERE clan_rank='{clan_rank}'")

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

            if len(discord_ids) > 0:
                discord_id = discord_ids[0]
                discord_name = discord_names[0]
                pg_id = pg_ids[0]
                pg_name = pg_names[0]
                clan_rank = clan_ranks[0]
                valor = valors[0]

                with open("./obey database/user_query.json", "r") as f:
                    user_query = json.load(f)

                with open("./obey database/user_query.json", "w") as f:
                    user_query.update({str(ctx.user.id):{"data":data,"page":0}})
                    json.dump(user_query, f, indent=1)

                member = ctx.guild.get_member(discord_id)

                user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
                user_info.set_thumbnail(url=member.display_avatar)
                user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
                user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            if len(data["discord_ids"]) > 1:
                await ctx.followup.send(embed=user_info, view=MembersListButtons())
            elif len(data["discord_ids"]) == 1:
                await ctx.followup.send(embed=user_info)
            else:
                await ctx.followup.send("Nothing found!")
    @app_commands.command(description="Search member by his name, id exist bot return all members with that name")
    async def custom_rank(self, ctx: discord.Interaction, custom_rank:str="Clan Member"):
        await ctx.response.defer()

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
            cursor.execute(f"SELECT * FROM members WHERE clan_rank='{custom_rank}'")

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

            if len(discord_ids) > 0:
                discord_id = discord_ids[0]
                discord_name = discord_names[0]
                pg_id = pg_ids[0]
                pg_name = pg_names[0]
                clan_rank = clan_ranks[0]
                valor = valors[0]

                with open("./obey database/user_query.json", "r") as f:
                    user_query = json.load(f)

                with open("./obey database/user_query.json", "w") as f:
                    user_query.update({str(ctx.user.id):{"data":data,"page":0}})
                    json.dump(user_query, f, indent=1)

                member = ctx.guild.get_member(discord_id)

                user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
                user_info.set_thumbnail(url=member.display_avatar)
                user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
                user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            if len(data["discord_ids"]) > 1:
                await ctx.followup.send(embed=user_info, view=MembersListButtons())
            elif len(data["discord_ids"]) == 1:
                await ctx.followup.send(embed=user_info)
            else:
                await ctx.followup.send("Nothing found!")

    @app_commands.command(description="Search member by his name, id exist bot return all members with that name")
    async def all(self, ctx: discord.Interaction, limit:str="None"):
        await ctx.response.defer()

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

            if limit=="None":
                cursor.execute(f"SELECT * FROM members")
            if limit.isnumeric():
                cursor.execute(f"SELECT * FROM members LIMIT {limit}")

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

            if len(discord_ids) > 0:
                discord_id = discord_ids[0]
                discord_name = discord_names[0]
                pg_id = pg_ids[0]
                pg_name = pg_names[0]
                clan_rank = clan_ranks[0]
                valor = valors[0]

                with open("./obey database/user_query.json", "r") as f:
                    user_query = json.load(f)

                with open("./obey database/user_query.json", "w") as f:
                    user_query.update({str(ctx.user.id):{"data":data,"page":0}})
                    json.dump(user_query, f, indent=1)

                member = ctx.guild.get_member(discord_id)

                user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
                user_info.set_thumbnail(url=member.display_avatar)
                user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
                user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            if len(data["discord_ids"]) > 1:
                await ctx.followup.send(embed=user_info, view=MembersListButtons())
            elif len(data["discord_ids"]) == 1:
                await ctx.followup.send(embed=user_info)
            else:
                await ctx.followup.send("Nothing found!")

    @app_commands.command(description="Search member by his name, id exist bot return all members with that name")
    async def yourself(self, ctx: discord.Interaction):
        await ctx.response.defer()

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

            cursor.execute(f"SELECT * FROM members WHERE discord_id={ctx.user.id}")

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

            if len(discord_ids) > 0:
                discord_id = discord_ids[0]
                discord_name = discord_names[0]
                pg_id = pg_ids[0]
                pg_name = pg_names[0]
                clan_rank = clan_ranks[0]
                valor = valors[0]

                with open("./obey database/user_query.json", "r") as f:
                    user_query = json.load(f)

                with open("./obey database/user_query.json", "w") as f:
                    user_query.update({str(ctx.user.id):{"data":data,"page":0}})
                    json.dump(user_query, f, indent=1)

                member = ctx.guild.get_member(discord_id)

                user_info = discord.Embed(title=f"Info about {discord_name}", description=f"**PG ID:**\n{pg_id}\n\n**PG NAME:**\n{pg_name}\n\n**CLAN RANK:**\n{clan_rank}\n\n**VALOR POINTS:**\n{valor}", color=0xd80e4a)
                user_info.set_thumbnail(url=member.display_avatar)
                user_info.set_footer(text=f"Page 1/{len(discord_ids)}")
                user_info.set_author(name=discord_name,icon_url=member.display_avatar)

            if len(data["discord_ids"]) > 1:
                await ctx.followup.send(embed=user_info, view=MembersListButtons())
            elif len(data["discord_ids"]) == 1:
                await ctx.followup.send(embed=user_info)
            else:
                await ctx.followup.send("Nothing found!")

    @app_commands.command(description="Help command for search app commands")
    async def help(self, ctx: discord.Interaction):
        
        help_list = {
            "titles": ["/search member"],
            "descriptions":[
                "``****``"
            ]
        }

async def setup(client):
    client.tree.add_command(MojaGrupa(name="search", description="test"))