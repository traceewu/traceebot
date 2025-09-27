import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Path to your image (local file)
IMAGE_PATH = "/opt/traceebot/ohwow.gif"

intents = discord.Intents.default()
intents.message_content = True  # bot needs this to read messages

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "oh wow" in message.content.lower():
        # Upload a local file
        file = discord.File(IMAGE_PATH, filename="ohwow.gif")
        await message.channel.send(file=file)

    await bot.process_commands(message)

@bot.command(name="traceebot")
async def traceebot(ctx, action=None, *, status_text=None):
    if action != "status" or not status_text:
        await ctx.send("Usage: `!traceebot status <status text>`")
        return

    try:
        activity = discord.CustomActivity(name=status_text)
        await bot.change_presence(activity=activity, status=discord.Status.online)
        await ctx.send(f"Status updated to: `{status_text}`")
    except Exception as e:
        await ctx.send(f"U fucked something up! Here's the error: {e}")

bot.run(TOKEN)
