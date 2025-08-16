# imports fella
import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self, *, intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
#start commands fella
    async def setup_hook(self):
        import aiohttp
        @self.tree.command(name="cat", description="Sends a random cat image")
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
        @app_commands.user_install()
        async def cat(interaction: discord.Interaction):
            url = "https://api.thecatapi.com/v1/images/search"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        image_url = data[0]["url"]
                        await interaction.response.send_message(image_url)
                    else:
                        await interaction.response.send_message("no cat rn sorry")

        @self.tree.command(name="bunny", description="Sends a random bunny image")
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
        async def bunny(interaction: discord.Interaction):
            url = "https://api.bunnies.io/v2/loop/random/?media=gif,png"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        image_url = data["media"]["gif"] or data["media"]["poster"]
                        await interaction.response.send_message(image_url)
                    else:
                        await interaction.response.send_message("no bunny rn sorry")

        @self.tree.command(name="dog", description="Sends a random dog image")
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
        async def dog(interaction: discord.Interaction):
            url = "https://dog.ceo/api/breeds/image/random"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        image_url = data["message"]
                        await interaction.response.send_message(image_url)
                    else:
                        await interaction.response.send_message("no dog rn sorry")

        @self.tree.command(name="ping", description="replies with pong and ms")
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
        async def ping(interaction: discord.Interaction):
            latency = round(self.latency * 1000)
            await interaction.response.send_message(f"Pong {latency}ms")
        
        @self.tree.command(name="skibidi", description="sends skibidi")
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
        async def skibidi(interaction: discord.Interaction):
            skibidi_url = "https://tenor.com/nivubhLOE9J.gif"
            await interaction.response.send_message(skibidi_url)
        
        @self.tree.command(name="motho_special", description="alright alright alright listen listen")
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
        async def motho(interaction: discord.Interaction):
            await interaction.response.send_message("https://cdn.discordapp.com/attachments/1019474643649835068/1406025292090179715/cachedVideo.mp4?ex=68a0f698&is=689fa518&hm=c5f321bfe92abdfd09ff1ce805cb125988284f7bf86a2dc8ec5814e9113a025e&")

        @self.tree.command(name="me_when", description="me when i get my hands on you")
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
        async def me_when(interaction: discord.Interaction):
            await interaction.response.send_message("https://cdn.discordapp.com/attachments/1019474643649835068/1405292643415625808/Screenshot_20250812-194644_YouTube2.jpg?ex=68a0ef43&is=689f9dc3&hm=65f399a00d513884d677af8635092888161a6ba5d495aeea9eeb9ea64364496b&")

        @self.tree.command(name="random_number", description="generates a random number between 1 and 2,147,483,647")
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
        async def random_number(interaction: discord.Interaction):
            number = random.randint(1, 2147483647)
            await interaction.response.send_message(f"Random number generated: {int(number):,}")
# register commands fella
        await self.tree.sync()
        print("commands registered, one hour brotato")
#end commands fella
    async def on_ready(self):
        print("Signed in as the bot broseph stalin")
        

client = MyClient(intents=intents)
client.run(TOKEN)