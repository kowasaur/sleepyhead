from disnake.interactions import application_command
from disnake.ext import commands
from dotenv import load_dotenv
from os import getenv
import json
from sleep import Sleep

REMIND_TIMES = [
    "22:00", "22:30", "23:00", "23:30", "00:00", "00:15", "00:30", "00:45",
    "01:00", "01:10", "01:20", "01:30", "01:40", "01:50", "02:00"
]
Interaction = application_command.ApplicationCommandInteraction

try:
    with open("sleepers.json", "r") as f:
        sleepers = json.load(f)
except FileNotFoundError:
    sleepers = []

load_dotenv()

bot = commands.InteractionBot(test_guilds=[606730636866093066])


@bot.event
async def on_ready():
    print(f"Current sleepers are: {sleepers}")


def update_sleepers():
    with open("sleepers.json", "w") as f:
        json.dump(sleepers, f)


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
    update_sleepers()
    await inter.response.send_message("Registered!")


@bot.slash_command(description="Deregister yourself from the sleep reminders")
async def deregister(inter: Interaction):
    author = inter.author.id

    if author not in sleepers:
        await inter.response.send_message("You're already not registered")
        return

    sleepers.remove(author)
    update_sleepers()
    await inter.response.send_message("Deregistered")


# TODO: only send while online
async def remind_sleepers():
    sleep = Sleep()
    while True:
        await sleep.wait_until_next()
        for sleeper in sleepers:
            user = await bot.fetch_user(sleeper)
            await user.send("Sleep")


bot.loop.create_task(remind_sleepers())
bot.run(getenv("TOKEN"))
