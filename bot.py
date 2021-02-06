import json
import discord
import asyncio
import os
import time
from discord.ext import tasks
from foodlist import generate_jsonfile
from discord.ext import commands

with open("discord_conf.json") as discord_conf:
    token = json.load(discord_conf)["token"]

bot = commands.Bot(command_prefix=",")

@commands.cooldown(1.0, 60.0)
@bot.command()
@commands.is_owner()
async def json_generate(ctx):
    await ctx.channel.send("generating json")
    h = generate_jsonfile()
    if h == "success":
        await ctx.channel.send("json generated")
    elif h == "error":
        await ctx.channel.send("there was a error while making the json file")

@bot.command()
@commands.is_owner()
async def todo(ctx, arg, title="all", *args):
    print(arg)
    if arg == "add":
        data = ""   
        json_data = {}
        for s in args:  
            data += s
            data += " " 
        data = data[:-1]
        json_data.update({title:data})
        with open("todo.json", "r+", encoding='utf8') as file:
            data = json.load(file)
            data.update(json_data)
            file.seek(0)
            json.dump(data, file, ensure_ascii=False)
        """
        with open("todo.json",'w', encoding='utf8') as f: 
                #json.dump(json_data, f, ensure_ascii=False) 
                json.dump(json_data, f, indent=4, ensure_ascii=False)
        """

    elif arg == "list":
        print("test1")
        if title == "all":
            print("test2")
            embed=discord.Embed(title="TODO List", color=0x4d4d4d)
            print("test3")
            with open("todo.json", encoding="utf8" ) as h:
                print("test4")
                data = json.load(h)
                print("test5")
                for x in data:
                    print("test6")
                    embed.add_field(name=x, value=data[x], inline=False)
            print("test7")
            await ctx.send(embed=embed)
        else:
            """
            embed=discord.Embed(title="TODO List", color=0x4d4d4d)
            with open("todo.json", encoding="utf8" ) as h:
                data = json.load(h)
                for x in data:
                    embed.add_field(name=x, value=data[x], inline=False)
            """
    else:
        await ctx.channel.send("Unknown arg")




@bot.command(aliases=["fl","sapuska"])
async def foodlist(ctx, *args):
    skip=False
    if time.time() - os.stat("./data.json").st_mtime > 3000:
        h = generate_jsonfile()
        if h == "error":
            await ctx.channel.send("there was a error while making the json file")
            skip = True



    sapuska = ""

    if args == ():
        sapuska = "Viikon sapuskat"
        args = ["ma","ti","ke","to","pe"]
    date = ""
    dates = []
    ma_args = ["manantai","ma","mon","monday"]
    ti_args = ["tiistai","ti","tue","tues","tuesday"]
    ke_args = ["keskiviikko","ke","wed","weds","wednesday"]
    to_args = ["torstai","to","thu","thur","thurs","thursday"]
    pe_args = ["perjantai","pe","fri","friday"]
    help_args = ["help","apua","h"]

    for input_arg in args:
        date = input_arg.lower()
        if date in ma_args:
            if not "ma" in dates:
                dates.append("ma")
        elif date in ti_args:
            if not "ti" in dates:
                dates.append("ti")
        elif date in ke_args:
            if not "ke" in dates:
                dates.append("ke")
        elif date in to_args:
            if not "to" in dates:
                dates.append("to")
        elif date in pe_args:
            if not "pe" in dates:
                dates.append("pe")
        elif date in help_args:
            if not "help" in dates:
                dates.append("help")

    args = dates

    if args == []:
        embed=discord.Embed(title="",description="invalid argument where given\nsee ,foodlist help for help", color=0xFF5733)
        await ctx.send(embed=embed)
        skip = True


    if "help" in args:
        des = """
        ",foodlist help" to show this
        ",foodlist" to show all days
        ",foodlist specific day" to show a specific day
        valid days are ma ti ke to pe
        """
        embed=discord.Embed(title="food list",description=des, color=0xFF5733)
        await ctx.send(embed=embed)
        skip = True
        
    if not skip:
        with open("data.json", encoding='utf-8') as s:
            foodlist = json.load(s)
        print("test1")
        if not sapuska == "Viikon sapuskat":
            sapuska = "Sapuskat"
            if len(args) == 1:
                sapuska = "Tänä päivän Sapuskaa"
        
        embed=discord.Embed(title=sapuska, color=0xFF5733)
        
        args2 = ["ma","ti","ke","to","pe"]
        for x in args2: 
            if x in args:
                k = foodlist[x]
                foods = "\n"
                foods = foods.join(k[1:])
                embed.add_field(name=k[0], value=foods, inline=False)

        await ctx.send(embed=embed)


@bot.command()
@commands.is_owner()
async def cat(ctx, arg):
    nono_files = ["discord_conf.json","file"]
    if arg in nono_files:
        await ctx.channel.send("you cant open that. thats a nono file")
    else:
        try:
            k = open(arg, encoding='utf-8')
            h = k.read()
            k.close()
            style = ""
            if arg.endswith(".py"):
                style = "py"
            if arg.endswith(".json"):
                style = "json"
            await ctx.channel.send("```" + style + "\n" + h + "```")
        except Exception as e:
            await ctx.channel.send("Error:" + e)

@bot.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.channel.send("Restarting")
    await ctx.bot.logout()

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.channel.send("Shuttingdown")
    h = open("shutdown","w")
    h.write("")
    h.close()
    await ctx.bot.logout()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Command on cooldown, try again in: {round(error.retry_after)} seconds.")
    if isinstance(error, commands.NotOwner):
        await ctx.send(f"you aint the bot owener")

print("bot has started")
bot.run(token)