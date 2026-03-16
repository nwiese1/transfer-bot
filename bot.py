import discord
from discord.ext import commands
import asyncio

TOKEN = "MTQ4MzI0MDg2OTc3MDQzMjY3OA.GJIdF0.0lAasuZSgn7OOcGUfT8dzS9I3NxlgruL2NA5EI"

SOURCE_CHANNEL_ID = 899441010285903883
TARGET_CHANNEL_ID = 1476028689623027832

BATCH_SIZE = 10

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def migrate(ctx):

    await ctx.send("Starting migration...")

    source_channel = bot.get_channel(SOURCE_CHANNEL_ID)
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)

    messages = []

    async for message in source_channel.history(limit=None, oldest_first=True):

        if message.author.bot:
            continue

        timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")

        if message.content:
            formatted = f"[{timestamp}] {message.author}: {message.content}"
            messages.append(formatted)

    await ctx.send(f"Collected {len(messages)} messages. Sending...")

    for i in range(0, len(messages), BATCH_SIZE):

        batch = messages[i:i+BATCH_SIZE]

        for msg in batch:

            if len(msg) > 2000:
                msg = msg[:1990] + "..."

            await target_channel.send(msg)

        await asyncio.sleep(2)

    await ctx.send("Migration finished.")

bot.run(TOKEN)
