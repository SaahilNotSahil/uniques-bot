from discord.ext import commands

import db
from utils import logger


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db.Prefix(
            guild_name=guild.name,
            guild_id=str(guild.id),
            prefix="$"
        ).save()

        channel = guild.system_channel

        if channel is not None:
            await channel.send(f"Hola! I'm Uniques! Thanks for inviting me to {guild.name}.")
            await channel.send(
                "My default prefix is $.\nUse ```$setprefix <prefix>``` to change the prefix."
            )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel

        await channel.send(
            f"Welcome {member.mention} to {member.guild.name}! We hope you enjoy your stay :slight_smile:"
        )

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(
            f"Hello, {ctx.author.mention}! I'm Uniques, nice to meet you :smile:"
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel

        await channel.send(
            f"{member.display_name} has left {member.guild.name}. Hope they'll come back :slight_smile:"
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        db.Prefix.objects(guild_id=str(guild.id)).delete()


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        try:
            if msg.content.split()[0] == "prefix":
                if msg.mentions[0] == self.bot.user:
                    await msg.channel.send(
                        f"My prefix is {db.get_prefix_from_message(msg)}"
                    )
        except IndexError:
            pass

    @commands.command()
    async def setprefix(self, ctx, *, prefix):
        if db.Prefix.objects(guild_id=str(ctx.guild.id)):
            logger.info(f"Prefix for server {ctx.guild.name} already exists")

            pref = db.Prefix.objects.get(guild_id=str(ctx.guild.id))
            pref.prefix = prefix
            pref.save()
        else:
            db.Prefix(
                guild_name=ctx.guild.name,
                guild_id=str(ctx.guild.id),
                prefix=prefix
            ).save()

        name = ctx.message.guild.get_member(self.bot.user.id).display_name
        p = name.split()[-1]

        if p[0] == '(' and p[-1] == ')':
            await ctx.message.guild.get_member(self.bot.user.id).edit(
                nick=f"{' '.join(name.split()[:-1])} ({prefix})"
            )
        else:
            await ctx.message.guild.get_member(self.bot.user.id).edit(
                nick=f"{name} ({prefix})"
            )

        await ctx.send(f"Prefix successfully changed to {prefix}")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"My ping time is: {round(self.bot.latency * 1000)} ms")

    @commands.command(aliases=['git'])
    async def github(self, ctx):
        await ctx.send("https://github.com/XanderWatson/uniques-bot")


async def setup(bot):
    await bot.add_cog(Greetings(bot))
    await bot.add_cog(Settings(bot))
