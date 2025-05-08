import re
import discord
from discord.ext import commands

TOKEN = "YOUR_TOKEN_HERE"

try:
    BOT_ID = int("1368459497160310804")
    CHANNEL_ID = int("1368443153866297348")
except ValueError:
    raise RuntimeError("TARGET_BOT_ID and TARGET_CHANNEL_ID must be set to integer IDs")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

tracked_message_id: int | None = None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Targeting bot ID {BOT_ID} in channel ID {CHANNEL_ID}")

@bot.event
async def on_message(message: discord.Message):
    global tracked_message_id

    if message.author.id != BOT_ID or message.channel.id != CHANNEL_ID:
        return

    if "with" in message.content:
        emoji = message.content.split(": ")[1]
        print(emoji)
        tracked_message_id = message.id
        try:
            await message.add_reaction(emoji)
            print(f"[+] Reacted with {emoji} to message {message.id}")
        except Exception as e:
            print(f"[!] Failed to react: {e}")

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    global tracked_message_id

    if after.id != tracked_message_id:
        return
    if "with" in after.content:
        print(after.content)
        emoji = after.content.split(": ")[1]
        print(emoji)
        channel = after.channel

        try:
            msg = await channel.fetch_message(after.id)
            await msg.add_reaction(emoji)
            print(f"[+] Reacted with {emoji} to edited message {after.id}")
        except Exception as e:
            print(f"[!] Failed to react on edit: {e}")

if __name__ == "__main__":
    bot.run(TOKEN, reconnect=True)