from discord.ext import commands, tasks
import discord
from datetime import datetime
import random

client = commands.Bot(command_prefix=".")

status = ["Nem jacok semmit hagyal", "Roblox", "Gebedek", "Ezt most komolyan van aki elolvassa?",
            "En csak egy csicska vagyok, szerinted mit jacok?", "Fortnajtozok"]

blacklist = open("blacklist.txt", "r", encoding="utf-8")
words = []
for line in blacklist:
    words.append(line.strip())
blacklist.close()
mode = True

@client.event
async def on_ready():
    change_status.start()
    await client.change_presence(status=discord.Status.online)
    print(">>> [" + datetime.now().strftime("%H:%M:%S") + "]", "BOT IS RUNNING")

@tasks.loop(seconds=1800)
async def change_status():
    await client.change_presence(activity=discord.Game(random.choice(status)))
    print(">>> [" + datetime.now().strftime("%H:%M:%S") + "]", "Status changed!")

@commands.has_permissions(administrator=True)
@client.command()
async def off(message):
    server = message.guild
    global mode
    mode = False
    await message.send("Blacklist tuned off. Type '.off' to turn it on.")
    print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]",
          f"Blacklist has been turned off at:\nServer: {server}")

@commands.has_permissions(administrator=True)
@client.command()
async def on(message):
    server = message.guild
    global mode
    mode = True
    await message.send("Blacklist tuned on. Type '.off' to turn it off.")
    print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]",
          f"Blacklist has been turned on at:\nServer: {server}")

@commands.has_permissions(administrator=True)
@client.command()
async def add(message, word):
    server = message.guild
    blacklist = open("blacklist.txt", "a")
    word = str(word).lower()
    blacklist.write(f"\n{word}")
    print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]",
          f"Blacklist appended with {word} at:\nServer: {server}")

@client.event
async def on_message(message):
    server = message.guild
    text = str(message.content).lower().strip().split()
    if (mode == True):
        for i in range(len(words)):
            word = str(words[i])
            if word in text:
                print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]",
                      f"Blocked word in text!\nServer: {server}\nMessage: {message.content}")
                await message.delete()
    await client.process_commands(message)

@client.command()
async def ping(message):
    await message.send(f"*Pong!* My ping is: {round(client.latency * 1000)} ms")
    print(">>> [" + datetime.now().strftime("%H:%M:%S") + "]", "Ping!")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please fill in all requirements.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have permissions for using this command.")

client.run("TOKEN GOES HERE")
