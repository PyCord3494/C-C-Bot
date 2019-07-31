import discord
from discord.ext import commands
import asyncio

class Shop(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.items = [200000, 500000]


	@commands.group(invoke_without_command=True, pass_context=True)
	async def shop(self, ctx):
		if ctx.invoked_subcommand is None:
			if await self.bot.get_cog("Economy").accCheck(ctx.author.id) == False:
				embed = discord.Embed(title="C&C Bot: Shop", color=0xff0000, description="You must $start your account before you can use my commands.")
				await ctx.send(embed=embed)
				return

			embed = discord.Embed(title="C&C Bot: Shop", color=0xdfe324, description="ID            ITEMS                COST\n1   not seperated custom role!  200,000\n2     seperated custom role!    500,000\n----------------------------------------\nUse +shop buy <id>")
			await ctx.send(embed=embed)
			# await ctx.send("```ML\nID            ITEMS                COST\n" # the shop menu
			# 					+ "1   not seperated custom role!  200,000\n"
			# 					+ "2     seperated custom role!    500,000\n"
			# 					+ "----------------------------------------\n"
			# 					+ "Use +shop buy <id>\n```")

	@shop.command()
	async def buy(self, ctx, ID: int):
		currency = self.bot.get_cog("Economy").getCurrency()
		discordId = ctx.message.author.id
		if await self.bot.get_cog("Economy").accCheck(discordId) == False:
			embed = discord.Embed(title="C&C Bot: Shop", color=0xff0000, description="You must $start your account before you can use my commands.")
			await ctx.send(embed=embed)
			return
		if ID != 1 and ID != 2: # if ID isn't valid
			embed = discord.Embed(title="C&C Bot: Shop", color=0xff0000, description="Invalid item ID.")
			await ctx.send(embed=embed)
			return
		
		bal = self.bot.get_cog("Economy").getBal(discordId) # grabs balance
		price = self.items[ID - 1] # grabs price from array in __init__
		if bal < price: # if cost is too much
			embed = discord.Embed(title="C&C Bot: Shop", color=0xff0000, description=f"That will cost you {price} {currency}, but you only have {bal} {currency}")
			await ctx.send(embed=embed)
			return

		await self.bot.get_cog("Economy").editBal(discordId, -price) # subtract price from bal
		
		embed = discord.Embed(title="C&C Bot: Shop", color=0xdfe324, description="Purchase successful! I sent a message to <@435806214484393996> and he will be messaging you when he can. Please be patient. :)")
		await ctx.send(embed=embed)

		if ID == 1: # shop item #1
			await ctx.guild.owner.send(f"User {ctx.author.mention} ({ctx.author.id}) has purchased \"Not separated Custom Role!\" for {price} {currency}") 
		
		elif ID == 2: # shop item #2
			await ctx.guild.owner.send(f"User {ctx.author.mention} ({ctx.author.id}) has purchased \"Seperated Custom Role!\" for {price} {currency}") 

def setup(bot):
	bot.add_cog(Shop(bot))