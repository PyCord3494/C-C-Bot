import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import random

import time
import json


async def get_prefix(bot, message):
	with open(r"config.json", 'r') as f:
			config = json.load(f)

	prefix = config["prefix"]
	return prefix

class Utils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(invoke_without_command=True, pass_context=True)
	async def help(self, ctx):
		prefix = await get_prefix(self.bot, ctx.message)
		embed = discord.Embed(title="C&C self.bot Help", color=0xdfe324, description=f"**My prefix is {prefix}**")
		embed.add_field(name="Money", value=f"{prefix}balance\n{prefix}shop\n{prefix}send\n{prefix}leaderboard")
		embed.add_field(name="Make Money!", value= f"{prefix}work\n{prefix}crime\n{prefix}gamble\n{prefix}slots")
		embed.add_field(name="Free Money!", value= f"{prefix}daily")
		embed.add_field(name="_ _\nUtilities", value= f"{prefix}ping\n{prefix}botinfo")
		embed.set_footer(text="\nType +help <command> for more info")
		await ctx.send(embed=embed)


	@help.command()
	async def ping(self, ctx):
		embed = discord.Embed(title="C&C Bot Help: Daily", color=0xdfe324, description="View the server's response time.")
		await ctx.send(embed=embed)

	@help.command()
	async def botinfo(self, ctx):
		embed = discord.Embed(title="C&C Bot Help: Daily", color=0xdfe324, description="Learn more about me and my developer!")
		await ctx.send(embed=embed)

	@help.command()
	async def balance(self, ctx):
		embed = discord.Embed(title="C&C Bot Help: Balance", color=0xdfe324, description="Displays your balance in the server. You can also type `+bal`")
		await ctx.send(embed=embed)

	@help.command()
	async def shop(self, ctx):
		embed = discord.Embed(title="C&C Bot Help: Shop", color=0xdfe324, description="Buy something from the shop! Type +shop for more details.")
		await ctx.send(embed=embed)

	@help.command()
	async def send(self, ctx):
		embed = discord.Embed(title="C&C Bot Help: Send", color=0xdfe324, description="Send money to someone else in the server.\nUsage: `+send <user> <amount>`\nType +send for more details.")
		await ctx.send(embed=embed)

	@help.command()
	async def leaderboard(self, ctx):
		embed = discord.Embed(title="C&C Bot Help: Daily", color=0xdfe324, description="Show the users with the most money in the server! You can also type `+lb`")
		await ctx.send(embed=embed)

	@help.command()
	async def work(self, ctx):
		embed = discord.Embed(title="C&C Bot Help: Work", color=0xdfe324, description="Use this command to quickly earn some money risk-free.")
		await ctx.send(embed=embed)

	@help.command()
	async def crime(self, ctx):
		embed = discord.Embed(title="C&C Bot Help: Crime", color=0xdfe324, description="Try to commit a crime to earn some money.\nUsage: `+crime`")
		await ctx.send(embed=embed)

	@help.command()
	async def gamble(self, ctx):
		embed = discord.Embed(title="C&C Bot Help: Gamble", color=0xdfe324, description="Risk some of your money to win some money.\nUsage: `+gamble amnt`")
		await ctx.send(embed=embed)

	@help.command()
	async def slots(self, ctx):
		embed = discord.Embed(title="C&C Bot Help: Gamble", color=0xdfe324, description="Risk some of your money and play the slot machine.\nUsage: `+slots amnt`")
		await ctx.send(embed=embed)

	@help.command()
	async def daily(self, ctx):
		embed = discord.Embed(title="C&C Bot Help: Daily", color=0xdfe324, description="Claim your daily reward!")
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Utils(bot))