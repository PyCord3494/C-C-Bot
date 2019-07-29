import discord
from discord.ext import commands
import asyncio

class Shop(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.items = [200000, 500000]


	@commands.group(invoke_without_command=True, pass_context=True)
	async def shop(self, ctx):
		if await self.bot.get_cog("Economy").accCheck(ctx.author.id) == False:
			await ctx.send("You must $start your account before you can buy stuff.")
			return

		if ctx.invoked_subcommand is None:
			await ctx.send("```ML\nID            ITEMS                COST\n"
								+ "1   not seperated custom role!  200,000\n"
								+ "2     seperated custom role!    500,000\n"
								+ "----------------------------------------\n"
								+ "Use +shop buy <id>\n```")

	@shop.command()
	async def buy(self, ctx, ID: int):
		currency = self.bot.get_cog("Economy").getCurrency()
		discordId = ctx.message.author.id
		if await self.bot.get_cog("Economy").accCheck(discordId) == False:
			await ctx.send("You must $start your account before you can buy stuff.")
			return
		if ID != 1 and ID != 2:
			await ctx.send("Invalid item ID.")
			return
		
		bal = self.bot.get_cog("Economy").getBal(discordId)
		price = self.items[ID - 1]
		if bal < price:
			await ctx.send(f"That will cost you {price} {currency}, but you only have {bal} {currency}")
			return

		await self.bot.get_cog("Economy").editBal(discordId, -price)
		
		if ID == 1:
			guildOwner = await self.bot.fetch_user(547475078082985990)
			await guildOwner.send(f"User {ctx.author.mention} ({ctx.author.id}) has purchased \"Not separated Custom Role!\" for {price} {currency}") 
		elif ID == 2:
			guildOwner = await self.bot.fetch_user(547475078082985990)
			await guildOwner.send(f"User {ctx.author.mention} ({ctx.author.id}) has purchased \"Seperated Custom Role!\" for {price} {currency}") 

def setup(bot):
	bot.add_cog(Shop(bot))