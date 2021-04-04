import random

import aiohttp
import discord
from discord.ext import commands

from utils import run, runCommand


class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ide(self, ctx):
        await ctx.send("Select ide mode (channel/dm):")

        ideMode = await self.bot.wait_for(
            'message', check=lambda message: message.author == ctx.author
        )
        ideMode = ideMode.content

        if ideMode == "channel":
            await ctx.send("Your ide mode is now set to channel.")
            await ctx.send(
                "Name of your code file (without extension)?"
            )

            filename = await self.bot.wait_for(
                'message', check=lambda message: message.author == ctx.author
            )
            filename = filename.content

            while True:
                langlist = ["c", "c++", "cpp", "py", "python"]

                await ctx.send(
                    "Select a programming language: c, cpp/c++, python/py"
                )

                language = await self.bot.wait_for(
                    'message',
                    check=lambda message: message.author == ctx.author
                )
                lang = language.content

                if lang in langlist:
                    break
                else:
                    await ctx.send(
                        "This programming language is either not recognized or not supported. Please try again."
                    )

            ext = ""
            if lang == "python" or lang == "py":
                ext = "py"
            elif lang == "c":
                ext = "c"
            elif lang == "c++" or lang == "cpp":
                ext = "cpp"

            await ctx.send(
                "Enter your code here (enclosed within three times '`'): "
            )

            msg = await self.bot.wait_for(
                'message', check=lambda message: message.author == ctx.author
            )

            if msg.content[0:3] == '```' and \
                    msg.content[len(msg.content) - 3:] == '```':
                code = msg.content[3:len(msg.content) - 3]

            await ctx.send("Type 'run' to run this code.")

            toRun = await self.bot.wait_for(
                'message', check=lambda message: message.author == ctx.author
            )

            outputs = []
            if toRun.content == "run":
                outputs = run(filename, ext, lang, code)

                await ctx.send(f"CompileError:\n{outputs[0]}")
                await ctx.send(f"Output:\n{outputs[1]}")
                await ctx.send(f"RuntimeError:\n{outputs[2]}")

        if ideMode == "dm":
            await ctx.send("Your ide mode is now set to dm.")
            await ctx.author.send(
                "Name of your code file (without extension)?"
            )

            filename = await self.bot.wait_for(
                'message', check=lambda message: message.author == ctx.author
            )
            filename = filename.content

            while True:
                langlist = ["c", "c++", "cpp", "py", "python"]

                await ctx.author.send(
                    "Select a programming language: c, cpp/c++, python/py"
                )

                language = await self.bot.wait_for(
                    'message',
                    check=lambda message: message.author == ctx.author
                )
                lang = language.content

                if lang in langlist:
                    break
                else:
                    await ctx.author.send(
                        "This programming language is either not recognized or not supported. Please try again."
                    )

            ext = ""
            if lang == "python" or lang == "py":
                ext = "py"
            elif lang == "c":
                ext = "c"
            elif lang == "c++" or lang == "cpp":
                ext = "cpp"

            await ctx.author.send(
                "Enter your code here (enclosed within three times '`'): "
            )

            msg = await self.bot.wait_for(
                'message', check=lambda message: message.author == ctx.author
            )

            if msg.content[0:3] == '```' and \
                    msg.content[len(msg.content) - 3:] == '```':
                code = msg.content[3:len(msg.content) - 3]

            await ctx.author.send("Type 'run' to run this code.")

            toRun = await self.bot.wait_for(
                'message', check=lambda message: message.author == ctx.author
            )

            outputs = []
            if toRun.content == "run":
                outputs = run(filename, ext, lang, code)

                await ctx.author.send(f"CompileError:\n`{outputs[0]}`")
                await ctx.author.send(f"Output:\n`{outputs[1]}`")
                await ctx.author.send(f"RuntimeError:\n`{outputs[2]}`")

    @commands.command(aliases=['term'])
    async def terminal(self, ctx):
        await ctx.send("Welcome to Uniques Terminal!")

        while True:
            await ctx.send(f"{str(ctx.author).split('#')[0]}@Uniques:~$")

            comm = await self.bot.wait_for(
                'message', check=lambda message: message.author == ctx.author
            )
            comm = comm.content

            if comm == "exit":
                await ctx.send("Exiting Uniques Terminal.")
                break
            else:
                outputs = runCommand(comm.split())

                if outputs[0] != '':
                    if len(outputs[0]) > 2000:
                        j = 0

                        for _ in range(len(outputs[0]) // 2000 + 1):
                            await ctx.send(
                                f"Output:\n`{outputs[0][j:j + 1990]}`"
                            )

                            j += 1990
                    else:
                        await ctx.send(f"Output:\n`{outputs[0]}`")

                if outputs[1] != '':
                    await ctx.send(f"Error:\n`{outputs[1]}`")

    @commands.command(aliases=['progmeme', 'pm'])
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                "https://www.reddit.com/r/programmerhumour.json"
            ) as r:
                meme = await r.json()

                meme_url = meme["data"]["children"][random.randint(1, 25)]
                meme_url = meme_url["data"]["url"]

                embed = discord.Embed(
                    color=discord.Color.blue(),
                )
                embed.set_image(url=meme_url)
                embed.set_footer(text=f"Meme requested by {ctx.author}")

                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Developer(bot))
