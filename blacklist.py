import discord
import asyncio
from discord.ext import commands

client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    print("msgrec bot is ready!")
    file1 = open("messages.txt", "a")
    file1.write(f"-------------------------------------------------------------------\n")
    file1.close()

@client.event
async def on_message(message):
    users_id = message.author.id
    channel = message.channel
    time = message.created_at
    server = message.guild
    attachments = message.attachments
    fetchMessage = await channel.history().find(lambda m: m.author.id == users_id)
    text = (f"----------{message.author}----------\nüzenet: {fetchMessage.content}\nserver: {server}\ncsatolt file-ok: {attachments}\ndátum: {time}\n========================================")
    file1 = open("messages.txt", "a", encoding="utf-8")
    file1.write(f"{text} \n")
    file1.close()

@client.event
async def on_message_delete(message):
    users_id = message.author.id
    channel = message.channel
    time = message.created_at
    server = message.guild
    attachments = message.attachments
    fetchMessage = await channel.history().find(lambda m: m.author.id == users_id)
    text = (f"----------[{message.author} DELETED A MESSAGE]----------\ntörölt üzenet: {fetchMessage.content}\nserver: {server}\ncsatolt file-ok: {attachments}\ndátum: {time}\n========================================")
    print(text)
    file1 = open("messages.txt", "a", encoding="utf-8")
    file1.write(f"{text} \n")
    file1.close()


client.run(TOKEN GOES HERE)
