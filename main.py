import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import db
from utils import handler, logger

load_dotenv()

db.connect()

intents = discord.Intents.all()
client = commands.Bot(command_prefix=db.get_prefix, intents=intents)


@client.event
async def on_ready():
    logger.info("Unique's Ready!")

    await client.load_extension('cogs.basic')
    await client.load_extension('cogs.developer')


@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    if extension == "help":
        client.remove_command("help")

    await client.load_extension(f'cogs.{extension}')

    await ctx.send(f"Loaded extension: {extension}.")


@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')

    if extension == "help":
        client.help_command = commands.DefaultHelpCommand()

    await ctx.send(f"Unloaded extension: {extension}.")


@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    await client.reload_extension(f'cogs.{extension}')


if __name__ == '__main__':
    client.run(
        token=os.getenv('DISCORD_TOKEN'),
        log_handler=handler,
        log_level=logging.INFO
    )
