from discord.ext import commands, tasks

import json
import discord
import asyncio
from meme import meme
import os
import time, functools
import schedule


from foodlist import generate_jsonfile


with open("./configs/discord_conf.json") as discord_conf:
    token = json.load(discord_conf)["token"]

bot = commands.Bot(command_prefix=",")

@commands.cooldown(1.0, 60.0)
@bot.command()
@commands.is_owner()
async def json_generate(ctx):
    await ctx.channel.send("generating json")
    h = await bot.loop.run_in_executor(None, functools.partial(generate_jsonfile))
    if h == "success":
        await ctx.channel.send("json generated")
    elif h == "error":
        await ctx.channel.send("there was a error while making the json file")

        
@bot.command()
@commands.is_owner()
async def todo(ctx, arg, title="all", *args):
    if arg == "add":
        data = ""   
        json_data = {}
        for s in args:  
            data += s
            data += " " 
        data = data[:-1]
        json_data.update({title:data})
        embed=discord.Embed(title="Added TODO", color=0x4d4d4d)
        embed.add_field(name=title, value=data, inline=False)
        with open("./data/todo.json", "r+", encoding='utf8') as f:
            data = json.load(f)
            data.update(json_data)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False)
        await ctx.send(embed=embed)

    elif arg == "list":
        if title == "all":
            with open("./data/todo.json", encoding='utf-8') as s:
                data = json.load(s)
            embed=discord.Embed(title="TODO List", color=0x4d4d4d)
            if data == {}:
                embed.add_field(name="TODO List is empty", value="Use ,todo add (title) (note)", inline=False)
            for x in data:
                embed.add_field(name=x, value=data[x], inline=False)
            await ctx.send(embed=embed)
        else:
            """
            embed=discord.Embed(title="TODO List", color=0x4d4d4d)
            with open("./data/todo.json", encoding="utf8" ) as h:
                data = json.load(h)
                for x in data:
                    embed.add_field(name=x, value=data[x], inline=False)
            """
    elif arg == "del":
        with open("./data/todo.json", encoding='utf-8') as s:
            data = json.load(s)
        try:
            h1 = data[title]
            data.pop(title)
            with open("./data/todo.json",'w', encoding='utf8') as f: 
                json.dump(data, f, ensure_ascii=False) 
            embed=discord.Embed(title="Deleted todo " + title , color=0xFF5733)
            embed.add_field(name=title, value=h1, inline=False)
        except:
            embed=discord.Embed(title="There is no " + title, color=0xFF5733)
        await ctx.send(embed=embed)

    else:
        await ctx.channel.send("unknown arg")

        
@bot.command(aliases=["r","meme"])
@commands.is_owner()
async def reddit(ctx, command):
    is_logged_aliases = ["islogged","is_logged","is_logged_in"]
    if command in is_logged_aliases:
        print(meme.is_logged)
        await ctx.channel.send(meme.is_logged())
    else:
        await ctx.channel.send("unknow command")

        
@bot.command(aliases=["fl","sapuska"])
async def foodlist(ctx, *args):
    skip=False
    if time.time() - os.stat("./data/foods.json").st_mtime > 3000:
        h = await bot.loop.run_in_executor(None, functools.partial(generate_jsonfile))
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
        embed=discord.Embed(title="food list",description=des, color=0x4d4d4d)
        await ctx.send(embed=embed)
        skip = True
        
    if not skip:
        with open("./data/foods.json", encoding='utf-8') as s:
            foodlist = json.load(s)
        if not sapuska == "Viikon sapuskat":
            sapuska = "Sapuskat"
            if len(args) == 1:
                sapuska = "Tänä päivän Sapuskaa"
        
        embed=discord.Embed(title=sapuska, color=0x4d4d4d)
        
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
    await ctx.bot.logout()

"""
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Command on cooldown, try again in: {round(error.retry_after)} seconds.")
    if isinstance(error, commands.NotOwner):
        await ctx.send(f"you aint the bot owener")

"""
print("Logged in Titityy")
bot.run(token)
