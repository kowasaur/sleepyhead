from disnake import interactions, Status, Intents, MemberCacheFlags
from disnake.ext import commands
from dotenv import load_dotenv
from os import getenv
import json
from sleep import Sleep

Interaction = interactions.application_command.ApplicationCommandInteraction

try:
    with open("data.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"sleepers": [], "guilds": []}

load_dotenv()
sleepers: list[int] = data["sleepers"]
guilds: list[int] = data["guilds"]  # repsective guilds of each sleeper
bot = commands.InteractionBot(intents=Intents.all())


@bot.event
async def on_ready():
    print(f"Current sleepers are: {sleepers}")


def update_sleepers():
    with open("data.json", "w") as f:
        json.dump({"sleepers": sleepers, "guilds": guilds}, f)


@bot.slash_command(description="What does this bot do?")
async def info(inter: Interaction):
    await inter.response.send_message(
        f"If you register, it sends reminders for you to go to sleep (if you're online) at these times: {Sleep.REMIND_TIMES}"
    )


@bot.slash_command(description="Register to be reminded to go to sleep")
async def register(inter: Interaction):
    author = inter.author.id

    if author in sleepers:
        await inter.response.send_message("You're already registered")
        return

    sleepers.append(author)
    guilds.append(inter.guild_id)
    update_sleepers()
    await inter.response.send_message("Registered!")


@bot.slash_command(description="Deregister yourself from the sleep reminders")
async def deregister(inter: Interaction):
    author = inter.author.id

    if author not in sleepers:
        await inter.response.send_message("You're already not registered")
        return

    index = sleepers.index(author)
    sleepers.pop(index)
    guilds.pop(index)
    update_sleepers()
    await inter.response.send_message("Deregistered")


async def remind_sleepers():
    sleep = Sleep()
    while True:
        await sleep.wait_until_next()
        for i, sleeper in enumerate(sleepers):
            guild = bot.get_guild(guilds[i])
            member = guild.get_member(sleeper)
            if member.status != Status.offline:
                await member.send("Sleep")


bot.loop.create_task(remind_sleepers())
bot.run(getenv("TOKEN"))
