import json
import discord
import asyncio
import os
import time
from discord.ext import tasks
from foodlist import generate_jsonfile
from discord.ext import commands

#test

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
            print("test2")
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
async def shutdown(ctx):
    await ctx.channel.send("Shuttingdown")
    #await asyncio.sleep(5)
    await ctx.bot.logout()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Command on cooldown, try again in: {round(error.retry_after)} seconds.")


bot.run(token)