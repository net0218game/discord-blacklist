from discord.ext import commands, tasks
import discord
from datetime import datetime
import random

client = commands.Bot(command_prefix=".")

status = ["Nem jacok semmit hagyal", "Roblox", "Gebedek", "Ezt most komolyan van aki elolvassa?",
          "En csak egy csicska vagyok, szerinted mit jacok?", "Fortnajtozok"]

# Blacklisted words list
blacklist = open("blacklist.txt", "r", encoding="utf-8")
words = []
for line in blacklist:
    words.append(line.strip())
blacklist.close()

# Member Blacklist list
memberlist = open("memberlist.txt", "r", encoding="utf-8")
members = []
for line in memberlist:
    members.append(line.strip())
memberlist.close()

# Word Blacklist
mode = True
# Member Blacklist
mode2 = True


@client.event
async def on_ready():
    change_status.start()
    await client.change_presence(status=discord.Status.online)
    print(">>> [" + datetime.now().strftime("%H:%M:%S") + "]", "BOT IS RUNNING")


@tasks.loop(seconds=1800)
async def change_status():
    await client.change_presence(activity=discord.Game(random.choice(status)))
    print(">>> [" + datetime.now().strftime("%H:%M:%S") + "]", "Status changed!")

# Turn on Blacklist function
@commands.has_permissions(administrator=True)
@client.command()
async def on(message):
    server = message.guild
    global mode
    mode = True
    await message.send("Blacklist tuned on. Type '.off' to turn it off!")
    print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]",
          f"Blacklist has been turned on at:\nServer: {server}")

# Turn off Blacklist function
@commands.has_permissions(administrator=True)
@client.command()
async def off(message):
    server = message.guild
    global mode
    mode = False
    await message.send("Blacklist tuned off. Type '.on' to turn it on!")
    print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]",
          f"Blacklist has been turned off at:\nServer: {server}")

# Turn on member Blacklist function
@commands.has_permissions(administrator=True)
@client.command()
async def on2(message):
    server = message.guild
    global mode2
    mode2 = True
    await message.send("Member Blacklist tuned on. Type '.off2' to turn it off!")
    print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]",
          f"Member Blacklist has been turned on at:\nServer: {server}")

# Turn off member Blacklist function
@commands.has_permissions(administrator=True)
@client.command()
async def off2(message):
    server = message.guild
    global mode2
    mode2 = False
    await message.send("Member Blacklist tuned off. Type '.on2' to turn it on!")
    print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]",
          f"Member Blacklist has been turned off at:\nServer: {server}")


# Add word to Blacklist
@commands.has_permissions(administrator=True)
@client.command()
async def add(message, word):
    server = message.guild
    blacklist = open("blacklist.txt", "a")
    word = str(word).lower()
    blacklist.write(f"\n{word}")
    print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]",
          f"Blacklist appended with {word} at:\nServer: {server}")
    blacklist.close()

# Remove word from Blacklist
@commands.has_permissions(administrator=True)
@client.command()
async def remove(message, word):
    server = message.guild
    blacklist = open("blacklist.txt", "a")
    for line in blacklist:
        if(word in line):
            line.replace("")

# Add people to Blacklist
@commands.has_permissions(administrator=True)
@client.command()
async def addmember(message, member: discord.Member):
    server = message.guild
    memberlist = open("memberlist.txt", "a")
    memberlist.write(f"\n{member.id}")
    print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]",
          f"{member} has been added to the Member Blacklist by {message.author}:\nServer: {server}")
    memberlist.close()


# Check for Blacklisted words
@client.event
async def on_message(message):
    server = message.guild

    # word Blacklist function
    text = str(message.content).lower().strip().split()
    if (mode == True):
        for i in range(len(words)):
            word = str(words[i])
            if word in text:
                print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]",
                      f"Blocked word in text!\nServer: {server}\nMessage: {message.content}")
                await message.delete()

    # member Blacklist function
    if (mode2 == True):
        for i in range(len(members)):
            if (str(message.author) == members[i]):
                await message.delete()
                print(f">>> [" + datetime.now().strftime("%H:%M:%S") + "]",
                      f"Blocked member's message!\nServer: {server}\nMessage: {message.content}\nAuthor: {message.author}")

    await client.process_commands(message)


# Ping command
@client.command()
async def ping(message):
    await message.send(f"*Pong!* My ping is: {round(client.latency * 1000)} ms")
    print(">>> [" + datetime.now().strftime("%H:%M:%S") + "]", "Ping!")


# Error messages
@client.event
async def on_command_error(ctx, error):
    server = ctx.guild
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command!")
        print(">>> [" + datetime.now().strftime("%H:%M:%S") + "]", f"Invalid command at\nServer: {server}")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please fill in all requirements.")
        print(">>> [" + datetime.now().strftime("%H:%M:%S") + "]", f"Missing requirements at\nServer: {server}")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have permissions for using this command.")


client.run("TOKEN GOES HERE")
