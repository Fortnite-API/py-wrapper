"""
This example demonstrates how to integrate the Fortnite API with a Discord bot using discord.py. 

The example creates a custom bot subclass that takes the Fortnite API client as an argument 
and stores it as an attribute. Then, a cog is created that holds some Fortnite-related commands. 
The cog uses the Fortnite API client to fetch the current main AES key.

Do not use the synchronous Fortnite API client with discord.py, as it will block the event loop.
"""

from __future__ import annotations

import asyncio
from typing import Optional

import discord
from discord.ext import commands

import fortnite_api


# Create a custom bot subclass that takes the Fortnite API client as an argument and stores it as an attribute.
# This is so that the Fortnite API client can be accessed from the bot instance.
class MyBot(commands.Bot):
    def __init__(self, fortnite_client: fortnite_api.FortniteAPI) -> None:
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.default(),
        )

        self.fortnite_client: fortnite_api.FortniteAPI = fortnite_client

    # When the bot is started, add the FortniteCog to the bot (defined below)
    async def setup_hook(self) -> None:
        await self.add_cog(FortniteCog())


# Create a cog that holds some Fortnite-related commands.
class FortniteCog(commands.Cog):

    # Define a command that fetches the current main AES key from the Fortnite API client.
    @commands.command(name='aes', description='Get the current main AES key, if any.')
    async def aes(self, ctx: commands.Context[MyBot]) -> None:
        # "ctx.bot" holds our custom bot subclass. Use it to access the Fortnite API client
        # and fetch the current main AES key.
        aes = await ctx.bot.fortnite_client.fetch_aes()
        main_key: Optional[str] = aes.main_key

        if main_key is None:
            await ctx.send('There is no AES main key available.')
        else:
            await ctx.send(f'The AES main key is: `{main_key}`')


# It is best for the fortnite_api.FortniteAPI client to be used with its async content manager,
# so create a start coroutine that will handle the setup and teardown of
# the Fortnite API client and the bot.
async def start() -> None:
    # Define the fortnite client and bot subclass
    fortnite_client = fortnite_api.FortniteAPI(api_key='YOUR_API_KEY')
    bot = MyBot(fortnite_client=fortnite_client)

    # Use the respective context managers
    async with fortnite_client, bot:
        # Start the discord bot
        await bot.start('YOUR_BOT_TOKEN')


# Start the bot only if the script is run directly.
if __name__ == '__main__':
    asyncio.run(start())
