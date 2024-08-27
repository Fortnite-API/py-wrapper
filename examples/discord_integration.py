"""
Discord Integration Example
---------------------------
This example demonstrates how to integrate the Fortnite API with a Discord bot using discord.py.
It walks you through the best practices to follow and how to structure your code to make the
most out of both libraries.

NOTE::
-------
Do NOT use the synchronous Fortnite API client with discord.py. It will block the event loop,
causing your Discord bot to become unresponsive. Always use the asynchronous client.
"""

from __future__ import annotations

import asyncio
import os
from typing import Optional

import discord
from discord.ext import commands

import fortnite_api


class MyBot(commands.Bot):
    """
    This is a custom Discord bot subclass that takes the Fortnite API client as an argument
    in its initializer and stores it as an attribute for later use.

    This is so that the Fortnite API client can be accessed anywhere the Discord bot
    instance is available.

    This is the recommended way to integrate the Fortnite API with discord.py.
    """

    # (1) Override __init__ to take the Fortnite API client as an argument.
    def __init__(self, fortnite_client: fortnite_api.Client) -> None:
        # (2) Call super() with the command prefix and intents.
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.default(),
        )

        # (3) And store the Fortnite API client as an attribute
        self.fortnite_client: fortnite_api.Client = fortnite_client

    # When the bot is started, add the FortniteCog to the bot (defined below)
    async def setup_hook(self) -> None:
        await self.add_cog(FortniteCog())


class FortniteCog(commands.Cog):
    """
    A commands.Cog instance that holds some Fortnite-related commands. In actuality,
    it is recommended for you to put your cogs in separate files, aka "extensions", for
    better organization.
    """

    @commands.command(name="aes", description="Get the current main AES key, if any.")
    async def aes(self, ctx: commands.Context[MyBot]) -> None:
        """
        A command that fetches the current main AES key using the Fortnite API client.
        """
        # (1) Get the current Discord bot
        bot: MyBot = ctx.bot

        # (2) Access our custom attribute to get the Fortnite API client
        fortnite_client: fortnite_api.Client = bot.fortnite_client

        # (3) fetch the AES key
        aes = await fortnite_client.fetch_aes()

        # (3.1) The main AES key is marked as optional in the documentation, so we must
        # handle the case where it is None.
        main_key: Optional[str] = aes.main_key

        # (4) and send a message back to the user.
        if main_key is None:
            await ctx.send("There is no AES main key available.")
        else:
            await ctx.send(f"The AES main key is: `{main_key}`")

    @commands.hybrid_command(
        name="total-cosmetics",
        description="Get the total number of cosmetics in Fortnite.",
    )
    async def total_cosmetics(self, ctx: commands.Context[MyBot]) -> None:
        """
        A hybrid command that uses the Fortnite API client to fetch
        the total number of cosmetics, including variants, in Fortnite.
        """
        # (1) Defer the response to acknowledge the command. Sometimes an API call can take
        # more than 3 seconds, so deferring is the only way to ensure the interaction
        # does not fail.
        async with ctx.typing():
            # (2) Get the current Discord bot
            bot: MyBot = ctx.bot

            # (3) Access our custom attribute to get the Fortnite API client
            fortnite_client: fortnite_api.Client = bot.fortnite_client

            # (4) Fetch all the Fortnite cosmetics
            all_cosmetics = await fortnite_client.fetch_cosmetics_all()

            # (4.1) We know that fortnite_api.CosmeticsAll has __len__ implemented
            # because we read the documentation, so we can use the built-in len() function.
            total_cosmetics = len(all_cosmetics)

            # (5) and send a message back to the user.
            await ctx.send(
                f"The total number of cosmetics in Fortnite is: `{total_cosmetics}`",
                ephemeral=True,
            )


async def main() -> None:
    """
    When working with both discord.py and fortnite_api, it is recommended to use a
    main function to start the bot. This function will handle the setup and teardown
    of the Fortnite API client and the Discord bot.

    In a real world example, this is also where you would set up any database connections
    or other services that your bot may need throughout its lifetime.
    """
    # (1) Define the fortnite client
    fortnite_client = fortnite_api.Client(api_key=os.environ["YOUR_API_KEY"])

    # (2) Create the bot instance
    bot = MyBot(fortnite_client=fortnite_client)

    # (3) Use the async context managers for both the Fortnite API client and the bot
    async with fortnite_client, bot:
        # (4) Start the bot
        await bot.start(os.environ["YOUR_BOT_TOKEN"])


# Start the bot only if the script is run directly.
if __name__ == "__main__":
    asyncio.run(main())
