import discord
from discord.ext import commands, tasks
import random
import asyncio
# import base64 # No longer needed for presence part
import os # For environment variables
import logging # Added for better error logging
# import time # No longer needed for transmission timing
from discord import DMChannel 

# --- Basic Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
log = logging.getLogger(__name__)

# --- Configuration ---
# TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = 'MTM2ODI4MzkwMDQ5Njk3Mzg3NA.GU7LQK.m-wvPUmazNbr8OCCRHb-S_NyfVEPvJa3oZDczg' # Replace with your actual bot token
if not TOKEN or TOKEN == 'YOUR_BOT_TOKEN':
    log.error("Discord bot token not found. Please set the TOKEN variable.")
    exit()

COMMAND_PREFIX = "!"
FLEETING_DURATION = 0.15 # Seconds the first flag part is visible
REACTION_TIMEOUT_PER_STEP = 0.8 # Seconds timeout for each emoji reaction
NUM_EMOJIS_TO_REACT = 7 # How many emojis the user needs to react to

# Morse/Presence Animation Config
PRESENCE_CHUNK_SIZE = 7 # Max characters to show in presence at once (as requested)
PRESENCE_UPDATE_INTERVAL = 5 # Seconds between presence updates (adjust as needed)
PRESENCE_ACTIVITY_TYPE = discord.ActivityType.watching # Changed to watching for "watching ..." effect

EXCLUDED_GUILD_ID = 1357627632707178719

# --- Flag Fragments ---
# UVT{F1R5T_3D1T_TH3N_R34CT_F1N4LLY_0B53RVE
FLAG_PART_1 = "UVT{F1R5T_3D1T"
FLAG_PART_2 = "_TH3N_R34CT_"
# Raw Morse code for "F1N4LLY_0B53RVE" -> ..-. .---- -. ....- .-.. .-.. -.-- ..--.- ----- -... ..... ...-- .-. ...- . ----.--
# Add spaces between Morse characters/groups for better visual separation in presence
FLAG_PART_3_MORSE = "..-. .---- -. ....- .-.. .-.. -.-- ..--.- ----- -... ..... ...-- .-. ...- ." # The morse for F1N4LLY_0B53RVE

# --- Bot Setup ---
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.presences = True # Needed for change_presence
intents.members = True # Needed potentially for DMing, getting author info

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)

# --- Global State for Presence Animation ---
presence_data_source = FLAG_PART_3_MORSE
presence_padding = " " * PRESENCE_CHUNK_SIZE # Padding for smooth scroll start/end
padded_presence_data = presence_padding + presence_data_source + presence_padding
presence_current_index = 0

# --- Helper Functions ---
async def send_dm(user: discord.User | discord.Member, content: str):
    """Attempts to send a DM, handles potential errors."""
    try:
        message = await user.send(content)
        # Limit logging length for potentially long messages
        log.info(f"Sent DM to {user.name} ({user.id}) with content: '{content[:70].replace(os.linesep, ' ')}...'")
        return message
    except discord.Forbidden:
        log.warning(f"Could not send DM to {user.name} ({user.id}). They may have DMs disabled or blocked the bot.")
        return None
    except discord.HTTPException as e:
        log.error(f"Failed to send DM to {user.name} ({user.id}): {e}")
        return None

# --- Background Task for Presence ---
@tasks.loop(seconds=PRESENCE_UPDATE_INTERVAL)
async def update_presence_task():
    """Continuously updates the bot's presence to scroll through the Morse code."""
    global FLAG_PART_3_MORSE, presence_current_index, padded_presence_data # Need to modify the global index

    # Calculate the chunk to display
    chunk = '| ' + FLAG_PART_3_MORSE[0:7].replace(" ", "_") + ' |'
    
    FLAG_PART_3_MORSE = FLAG_PART_3_MORSE[1:] + FLAG_PART_3_MORSE[0] # Rotate the string for the next chunk

    # Update presence
    activity = discord.Activity(type=PRESENCE_ACTIVITY_TYPE, name=chunk)
    try:
        await bot.change_presence(activity=activity)
        log.debug(f"Presence updated to: {chunk}") # Optional: very verbose logging
    except discord.HTTPException as e:
        log.error(f"Failed to update presence during continuous task: {e}")
        # Consider adding a longer sleep here if rate limited, but usually task loop handles it okay
    except Exception as e:
         log.error(f"Unexpected error changing presence in task: {e}", exc_info=True)

    # Increment index and loop back around
    presence_current_index += 1
    # Check if index reached the point where the chunk would go past the end of padded data
    if presence_current_index > len(padded_presence_data) - PRESENCE_CHUNK_SIZE:
        presence_current_index = 0 # Reset to the beginning

@update_presence_task.before_loop
async def before_update_presence_task():
    """Ensures the bot is ready before starting the presence loop."""
    await bot.wait_until_ready()
    log.info("Starting continuous presence update task.")

# --- Bot Events ---
@bot.event
async def on_ready():
    log.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    log.info('------')
    # Start the background task
    if not update_presence_task.is_running():
        update_presence_task.start()
    # Initial presence will be set by the first run of the task loop

# --- Commands ---

@bot.command(name='helpme')
async def help_command(ctx):
    """Provides help via DM and triggers the first part of the challenge."""
    author = ctx.author
    original_command_message = ctx.message

    initial_dm_content = (
        f"Hello {author.mention}! Available commands:\n"
        f"`{COMMAND_PREFIX}helpme` - This help message.\n"
        f"`{COMMAND_PREFIX}randomoji` - Start the reaction challenge (can be used in a server).\n"
        "I process things REALLY quickly! Did you fix a typo.. or did I just blink?\nIf you want to invite me to your own server you can use (To avoid Discord TOS): https://discord.com/oauth2/authorize?client_id=1368283900496973874&permissions=8&integration_type=0&scope=bot"
    )
    bot_dm_message = await send_dm(author, initial_dm_content)

    if bot_dm_message is None:
        log.warning(f"Failed to initiate helpme challenge for {author.name} due to DM failure.")
        return

    def check_edit(before, after):
        return before.id == original_command_message.id and after.author == author

    try:
        log.info(f"Waiting for {author.name} to edit message {original_command_message.id}...")
        before_msg, after_msg = await bot.wait_for('message_edit', timeout=15.0, check=check_edit)

        log.info(f"User {author.name} triggered Stage 1 via edit.")
        flag_reveal_content = f"Quick! `{FLAG_PART_1}`"
        await bot_dm_message.edit(content=flag_reveal_content)
        await asyncio.sleep(FLEETING_DURATION)
        neutral_content = "WHAT WAS THAT!!!? I didn't see anything...\n"
        try:
            await bot_dm_message.edit(content=neutral_content)
            log.info(f"Edited DM message {bot_dm_message.id} back after fleeting display for {author.name}.")
        except (discord.NotFound, discord.HTTPException) as e:
             log.warning(f"Could not edit DM {bot_dm_message.id} back after hint for {author.name}: {e}")

    except asyncio.TimeoutError:
        log.info(f"User {author.name} timed out waiting for message edit (Stage 1).")
        timeout_content = initial_dm_content.replace(
            "I process things REALLY quickly! Did you fix a typo.. or did I just blink?\n",
            "I process things REALLY quickly! Did you fix a typo.. or did I just *blink*?\n"
        )
        try:
            if bot_dm_message:
                await bot_dm_message.edit(content=timeout_content)
        except (discord.NotFound, discord.HTTPException) as e:
            log.warning(f"Could not edit DM {bot_dm_message.id} on timeout for {author.name}: {e}")


@bot.command(name='randomoji')
async def randomoji_command(ctx):
    """Sends a multi-step random emoji reaction challenge via DM for Flag Part 2."""
    author = ctx.author
    original_command_message_id = ctx.message.id

    possible_emojis = ['🤔', '✅', '🔑', '🤖', '👀', '🕵️', '🔒', '🔓', '⚡', '💡', '⭐', '💯', '🎯', '🏁', '🎁']
    if len(possible_emojis) < NUM_EMOJIS_TO_REACT:
        log.error(f"Config error: Not enough possible emojis ({len(possible_emojis)}) for sequence ({NUM_EMOJIS_TO_REACT}).")
        await send_dm(author, "Internal bot error: Emoji configuration issue.")
        return

    try:
        sequence_emojis = random.sample(possible_emojis, NUM_EMOJIS_TO_REACT)
    except ValueError:
        log.error("ValueError during random.sample for emojis.")
        await send_dm(author, "Internal bot error setting up the emoji game.")
        return

    log.info(f"Starting randomoji sequence for {author.name}: {sequence_emojis}")

    dm_challenge_content = f"Reaction Challenge! React to *this* message with exactly: {sequence_emojis[0]}"
    
    bot_dm_message = None
    if isinstance(ctx.channel, DMChannel):
        # user ran the command via DM
        bot_dm_message = await send_dm(ctx.author, dm_challenge_content)
    else:
        # user ran the command in a guild channel
        bot_dm_message = await ctx.channel.send(dm_challenge_content)

    if bot_dm_message is None:
        log.warning(f"Failed to initiate randomoji challenge for {author.name} due to DM failure.")
        return

    # No game_success variable needed, success path directly gives flag part 2
    for i in range(NUM_EMOJIS_TO_REACT):
        current_emoji = sequence_emojis[i]
        log.info(f"Waiting for {author.name} to react with {current_emoji} ({i+1}/{NUM_EMOJIS_TO_REACT}) on DM {bot_dm_message.id}...")

        def check_reaction(reaction, user):
            # Ensure the reaction is on the correct message, by the correct user, and is the correct emoji
            return (reaction.message.id == bot_dm_message.id and
                    str(reaction.emoji) == current_emoji)

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=REACTION_TIMEOUT_PER_STEP, check=check_reaction)
            log.info(f"User {author.name} correctly reacted with {current_emoji}.")

            if i < NUM_EMOJIS_TO_REACT - 1:
                next_emoji = sequence_emojis[i+1]
                next_prompt = f"Correct! Now react with: {next_emoji}"
                try:
                    await bot_dm_message.edit(content=next_prompt)
                    log.info(f"Edited DM {bot_dm_message.id} for {author.name} to prompt for {next_emoji}.")
                except (discord.NotFound, discord.HTTPException) as e:
                    log.warning(f"Could not edit DM {bot_dm_message.id} for next step: {e}")
                    await send_dm(author, "Something went wrong updating the challenge message! Make a ticket if you see this message.")
                    return # Exit command cleanly if DM edit fails

            else:
                # This is the last successful reaction
                log.info(f"User {author.name} completed the randomoji sequence.")
                # Give Flag Part 2 and hint for Stage 3 (observation)
                success_message = (
                    f"Excellent! Reaction sequence complete. Here's the next piece: `{FLAG_PART_2}`\n\n"
                )
                await send_dm(author, success_message)
                return # Exit command cleanly after success

        except asyncio.TimeoutError:
            log.info(f"User {author.name} timed out waiting for reaction {current_emoji} ({i+1}/{NUM_EMOJIS_TO_REACT}).")
            fail_message = f"Too slow reacting with {current_emoji}! Try the `{COMMAND_PREFIX}randomoji` command again."
            try:
                if bot_dm_message: await bot_dm_message.edit(content=fail_message)
            except (discord.NotFound, discord.HTTPException) as e:
                 log.warning(f"Could not edit DM {bot_dm_message.id} on reaction timeout for {author.name}: {e}")
            return # Exit command cleanly after timeout failure

        except Exception as e:
             log.error(f"Unexpected error during reaction wait for {author.name} on step {i+1}: {e}", exc_info=True)
             await send_dm(author, "An unexpected error occurred during the reaction game.")
             return # Exit command cleanly on unexpected error

# --- Removed transmit Command ---
# The `transmit` command is no longer needed as the presence update is continuous.

@bot.event
async def on_message(message):
    # never respond to bots
    if message.author.bot:
        return

    if message.guild and message.guild.id == EXCLUDED_GUILD_ID:
        return

    # only handle DMs
    if True: #isinstance(message.channel, DMChannel):
        # if it’s a “!…” command, let commands.py handle it
        if message.content.startswith(COMMAND_PREFIX):
            await bot.process_commands(message)
        # otherwise send the help text
        else:
            help_text = (
                f"Hello {message.author.mention}! maybe you could use {COMMAND_PREFIX}helpme\n If you want to invite me to your own server you can use (To avoid Discord TOS): https://discord.com/oauth2/authorize?client_id=1368283900496973874&permissions=8&integration_type=0&scope=bot"
            )
            await send_dm(message.author, help_text)
    # ignore everything else (no guild responses)
    else:
        return

# --- Error Handling ---
@bot.event
async def on_command_error(ctx, error):
    """Basic error handling, sends errors via DM if possible."""
    # Ignore checks failures and command not found for less noise
    if isinstance(error, (commands.CommandNotFound, commands.CheckFailure)):
        # Optionally log these if you want to track failed attempts
        log.debug(f"Command '{ctx.invoked_with}' failed check or not found for {ctx.author.name}: {error}")
        # Try to delete the invalid command message if it exists and we have perms
        try:
            await ctx.message.delete()
        except Exception:
            pass # Ignore delete errors here
        return

    author = ctx.author
    log.error(f"Error occurred for command '{ctx.command}' invoked by {author.name} ({author.id}): {error}", exc_info=isinstance(error, commands.CommandInvokeError))

    error_message = "An unexpected error occurred." # Default message
    if isinstance(error, commands.MissingRequiredArgument):
        error_message = f"Missing argument(s) for command `{ctx.command.name}`."
    elif isinstance(error, commands.CommandInvokeError):
        # Log the original error details, but give a generic message to the user
        log.error(f"Underlying error for {ctx.command.name}: {error.original}")
        error_message = "An internal error occurred while processing the command."
    elif isinstance(error, commands.CommandOnCooldown): # Example if you add cooldowns
        error_message = f"Command is on cooldown. Try again in {error.retry_after:.2f}s."
    elif isinstance(error, commands.UserInputError): # Broader category for bad input
        error_message = f"Invalid input for command `{ctx.command.name}`."

    await send_dm(author, f"Error: {error_message}")

    # Try to delete the failed command message
    try:
        await ctx.message.delete()
    except Exception:
        pass # Ignore delete errors here


# --- Run the Bot ---
if __name__ == "__main__":
    if TOKEN and TOKEN != 'YOUR_BOT_TOKEN':
        try:
            bot.run(TOKEN)
        except discord.PrivilegedIntentsRequired:
            log.error("Privileged intents (Message Content, Presence, Members) are NOT enabled for the bot in the developer portal. Please enable them!")
        except discord.LoginFailure:
             log.error("Failed to log in: Invalid Discord token provided.")
        except Exception as e:
             log.error(f"An unexpected error occurred during bot startup or runtime: {e}", exc_info=True)
    else:
        log.critical("Failed to start: Bot token is missing or placeholder.")
