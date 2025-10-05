import discord
from discord.ext import commands
import os
import nltk
from config import BOT_VERSION, DEFAULT_BOT_PREFIX, DISCORD_BOT_TOKEN
import asyncio
from infrastructure import PrefixRepository

# ----------------------------
# NLTK Data Setup
# ----------------------------
nltk_data = [
    'punkt',
    'punkt_tab',
    'stopwords',
    'averaged_perceptron_tagger',
    'averaged_perceptron_tagger_eng',
    'wordnet',
    'omw-1.4'
]

for data in nltk_data:
    try:
        nltk.data.find(data)
    except LookupError:
        nltk.download(data.split('/')[-1], quiet=True)
        print(f"Downloaded NLTK {data.split('/')[-1]}")

# ----------------------------
# Bot Setup
# ----------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

prefix_repo = PrefixRepository()
async def dynamic_prefix(bot, message):
    # default fallback
    default = DEFAULT_BOT_PREFIX

    if message.guild:
        prefix = await prefix_repo.get_by_guild_id(message.guild.id)
        return commands.when_mentioned_or(prefix or default)(bot, message)
    return commands.when_mentioned_or(default)(bot, message)

bot = commands.Bot(command_prefix=dynamic_prefix, intents=intents, help_command=None)

# ----------------------------
# Bot Events
# ----------------------------
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot v{BOT_VERSION} is ready with enhanced review system!')
    print(f'Connected to {len(bot.guilds)} guilds: {[guild.name for guild in bot.guilds]}')

@bot.event
async def on_command_error(ctx, error):
    print(f"❌ Error: Command error from {ctx.author}: {error}")

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Please provide all required arguments. Use `!help` for guidance.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.CommandNotFound):
        pass  # ignore unknown commands
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")
        print(f"❌ Error: Unexpected command error: {error}")

@bot.event
async def on_command(ctx):
    print(f"Command received: {ctx.command} from {ctx.author} in {ctx.guild.name if ctx.guild else 'DM'}")

@bot.event
async def on_command_completion(ctx):
    print(f"Command completed: {ctx.command} from {ctx.author}")

# ----------------------------
# Async Main Function
# ----------------------------
async def main():
    # Load cogs
    try:
        await bot.load_extension('api.cogs.admin')
        await bot.load_extension('api.cogs.review')
        await bot.load_extension('api.cogs.categories')
        await bot.load_extension('api.cogs.help')
        await bot.load_extension('api.cogs.tests')
        print("Successfully loaded all cogs")
    except Exception as e:
        print(f"❌ Error: Error loading cogs: {e}")

    # Start bot
    token = DISCORD_BOT_TOKEN
    if not token:
        print("❌ Error: DISCORD_BOT_TOKEN not set in configuration!")
        print("Please set your Discord bot token in the config.yaml file or as an environment variable.")
    else:
        print(f"Starting bot v{BOT_VERSION}...")
        await bot.start(token)

# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    asyncio.run(main())