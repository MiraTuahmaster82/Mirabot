import discord, random, aiohttp
from discord import app_commands

async def setup_hook(bot):
	@bot.tree.command(name="cat", description="Sends a random cat image")
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

	@bot.tree.command(name="bunny", description="Sends a random bunny image")
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

	@bot.tree.command(name="dog", description="Sends a random dog image")
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

	@bot.tree.command(name="ping", description="replies with pong and ms")
	@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
	async def ping(interaction: discord.Interaction):
		latency = round(bot.latency * 1000)
		await interaction.response.send_message(f"Pong {latency}ms")
	
	@bot.tree.command(name="skibidi", description="sends skibidi")
	@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
	async def skibidi(interaction: discord.Interaction):
		skibidi_url = "https://tenor.com/nivubhLOE9J.gif"
		await interaction.response.send_message(skibidi_url)
	
	@bot.tree.command(name="motho_special", description="alright alright alright listen listen")
	@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
	async def motho(interaction: discord.Interaction):
		await interaction.response.send_message("[Motho Special](https://cdn.discordapp.com/attachments/1019474643649835068/1406025292090179715/cachedVideo.mp4?ex=68a0f698&is=689fa518&hm=c5f321bfe92abdfd09ff1ce805cb125988284f7bf86a2dc8ec5814e9113a025e&)")

	@bot.tree.command(name="me_when", description="me when i get my hands on you")
	@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
	async def me_when(interaction: discord.Interaction):
		await interaction.response.send_message("https://cdn.discordapp.com/attachments/1019474643649835068/1405292643415625808/Screenshot_20250812-194644_YouTube2.jpg?ex=68a0ef43&is=689f9dc3&hm=65f399a00d513884d677af8635092888161a6ba5d495aeea9eeb9ea64364496b&")

	@bot.tree.command(name="random_number", description="generates a random number between 1 and 2,147,483,647")
	@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
	async def random_number(interaction: discord.Interaction):
		number = random.randint(1, 2147483647)
		await interaction.response.send_message(f"Random number generated: {int(number):,}")
		
	@bot.tree.command(name="wikipedia", description="searches wikipedia for a term")
	@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
	@app_commands.describe(query="The term to search for on Wikipedia")
	async def wikipedia(interaction: discord.Interaction, query: str):
		search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
		async with aiohttp.ClientSession() as session:
			async with session.get(search_url) as resp:
				if resp.status == 200:
					data = await resp.json()
					title = data.get("title", "No title")
					extract = data.get("extract", "No summary brah")
					page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
					thumbnail = data.get("thumbnail", {}).get("source")
					embed = discord.Embed(title=title, description=extract, url=page_url, color=discord.Color.dark_green())
					if thumbnail:
						embed.set_thumbnail(url=thumbnail)
					await interaction.response.send_message(embed=embed)
				else:
					await interaction.response.send_message("no wiki page for that bro")

	@bot.tree.command(name="urban_dictionary", description="searches Urban Dictionary for a term")
	@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
	@app_commands.describe(query="The term to search for on Urban Dictionary")
	async def urban_dictionary(interaction: discord.Interaction, query: str):
		search_url = f"https://api.urbandictionary.com/v0/define?term={query}"
		async with aiohttp.ClientSession() as session:
			async with session.get(search_url) as resp:
				if resp.status == 200:
					data = await resp.json()
					if data["list"]:
						definition = data["list"][0]["definition"]
						example = data["list"][0]["example"]
						embed = discord.Embed(title=f"Definition of {query}", description=definition, color=discord.Color.dark_green())
						if example:
							embed.add_field(name="Example", value=example, inline=False)
						await interaction.response.send_message(embed=embed)
					else:
						await interaction.response.send_message("no definition found for that brotato")
				else:
					await interaction.response.send_message("error fetching from Urban Dictionary dawg")

# register commands fella
	await bot.tree.sync()