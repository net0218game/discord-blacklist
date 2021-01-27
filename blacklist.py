from discord.ext import commands, tasks
import discord
from datetime import datetime
import random

client = commands.Bot(command_prefix=".")

status = ["Nem jacok semmit hagyal", "Roblox", "Gebedek", "Ezt most komolyan van aki elolvassa?",
            "En csak egy csicska vagyok, szerinted mit jacok?", "Fortnajtozok"]

words = ["lol", "k", "ok"]

@client.event
async def on_ready():
    change_status.start()
    await client.change_presence(status=discord.Status.online)
    print(">>> [" + datetime.now().strftime("%H:%M:%S") + "]", "BOT IS RUNNING")

@tasks.loop(seconds=150)
async def change_status():
    await client.change_presence(activity=discord.Game(random.choice(status)))
    print(">>> [" + datetime.now().strftime("%H:%M:%S") + "]", "Status changed!")

@client.command()
async def ping(message):
    await message.send(f"*Pong!* My ping is: {round(client.latency * 1000)} ms")
    print(">>> [" + datetime.now().strftime("%H:%M:%S") + "]", "Ping!")

@client.event
async def on_message(message):
    server = message.guild
    text = str(message.content).strip().split()
    for i in range(len(words)):
        word = str(words[i])
        if word in text:
            print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]", f"Blocked word in text!\nServer: {server.id}\nMessage: {message.content}")
            await message.delete()

client.run("TOKEN GOES HERE")
