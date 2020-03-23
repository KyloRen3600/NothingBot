TOKEN = "METTRE LE TOKEN ICI"

import discord
from discord.ext import commands
import datetime
from random import choice
import string

class Game():
	def __init__(self, channel_id):
		log("INFO", "Starting new game on channel {0}".format(channel_id))
		self.channel_id = channel_id
		self.word = Word(choice_word())
		log("INFO", "Word is {0}".format(self.word.word))
		self.used_lifes = 0

	def try_letter(self, letter):
		test = self.word.reveal_letter(letter)
		if test == True:
			return True
		else:
			self.used_lifes += 1
			if self.used_lifes < 10:
				return False
			else:
				return "lost"
	def try_word(self, word):
		if self.word.word == word:
			return True
		else:
			self.used_lifes += 1
			if self.used_lifes < 10:
				return False
			else:
				return "lost"



class Word():
	def __init__(self, word):
		self.word = word
		self.hided = []
		self.revealed = 0
		i = 0
		while i < len(self.word):
			self.hided.append("-")
			i += 1
		self.used_lifes = 0

	def reveal_letter(self, letter):
		finded = False
		for i, l in enumerate(self.word):
			if l == letter:
				self.hided[i] = letter
				self.revealed += 1
				finded = True
		return finded

	def get_finded(self):
		return ''.join(self.hided)

	def is_finded(self):
		if len(self.word) == self.revealed:
			return True
		else:
			return False


def log(type, message):
	now = datetime.datetime.now()
	hour = now.hour
	if hour < 10:
		hour = "0{0}".format(hour)
	minute = now.minute
	if minute < 10:
		minute = "0{0}".format(minute)
	second = now.second
	if second < 10:
		second = "0{0}".format(second)
	now = "[{0}:{1}:{2}] [{3}]:".format(hour, minute, second, type)
	print("{0} {1}".format(now, message))


def choice_word():
	with open("words.txt", "r") as file:
		text = file.read()
		words = text.split()
		return choice(words).lower()


def build_embed(user, channel, color):
	embed = discord.Embed(title="[Pendu]",
	                      url="https://github.com/KyloRen3600/KyloBot/blob/master/Addons/Pendu/README.MD",
	                      color=color)
	embed.set_author(name=user.name, icon_url=user.avatar_url)
	embed.set_footer(text="Développé par KyloRen3600")
	try:
		game = games["{0}".format(channel)]
		if game.used_lifes < 10:
			embed.set_thumbnail(
				url="https://raw.githubusercontent.com/KyloRen3600/KyloBot/master/Addons/Pendu/pendu-etape0{0}.gif".format(
					game.used_lifes))
		else:
			embed.set_thumbnail(
				url="https://raw.githubusercontent.com/KyloRen3600/KyloBot/master/Addons/Pendu/pendu-etape{0}.gif".format(
					game.used_lifes))
	except:
		pass
	return embed


def get_help_embed(author, channel):
	embed = build_embed(author, channel, 0xffff00)
	embed.add_field(name="Aide:",
	                value="\"{0}start\" -> Commencer une partie\n\"{0}p\" -> Proposer une lettre/un mot\n\"{0}reveal\" -> Abandonner la partie".format(
		                prefix))
	return embed

def get_not_ingame_embed(author, channel):
	embed = build_embed(author, channel, 0xffff00)
	embed.add_field(name="Aucune partie en cours",
	                value="Faites \"{0}start\" pour commencer une partie.".format(prefix))
	return embed

prefix = "!"
games = {}
bot = commands.Bot(command_prefix=prefix)


@bot.listen()
async def on_message(message):
	log("MESSAGE", "<{0}> {1} > {2}".format(message.channel.id, message.author.name, message.content))


@bot.listen()
async def on_ready():
	await bot.change_presence(activity=discord.Streaming(name="Faites {0}aide pour obtenir l'aide".format(prefix),
	                                                     url="https://twitch.tv/KyloBot", type=1))
	log("INFO", "Status defined")


@bot.command()
async def ping(ctx):
	channel_id = ctx.message.channel.id
	await ctx.send(embed=get_not_ingame_embed(ctx.message.author, channel_id))


@bot.command()
async def start(ctx):
	channel_id = ctx.message.channel.id
	message = ctx.message
	try:
		game = games["{0}".format(channel_id)]
		embed = build_embed(message.author, message.channel.id, 0xffff00)
		embed.add_field(name="Partie déjà  lancée !", value="Faites \"{0}reveal\" pour abandonner.".format("!"),
		                inline=True)
		embed.add_field(name="Mot:", value=game.word.get_finded(), inline=False)
	except:
		games["{0}".format(channel_id)] = Game(channel_id)
		game = games["{0}".format(channel_id)]
		embed = build_embed(message.author, message.channel.id, 0x00ff00)
		embed.add_field(name="Partie lancée", value="Bonne chance !", inline=True)
		embed.add_field(name="Mot:", value=game.word.get_finded(), inline=True)
	await ctx.send(embed=embed)

@bot.command()
async def p(ctx, arg):
	channel_id = ctx.message.channel.id
	try:

		game = games["{0}".format(channel_id)]

		if len(arg) == 1:
			if any(arg in s for s in list(string.ascii_lowercase)):
				test =game.try_letter(arg)
				if test == True:
					if game.word.word == game.word.get_finded():
						embed = build_embed(ctx.message.author, ctx.message.channel.id, 0x00ff00)
						embed.add_field(name="Proposition:",
						                value="{0}\nLettre présente !\nPartie gagnée !".format(arg.upper()),
						                inline=True)
						embed.add_field(name="Mot:", value=game.word.word, inline=True)
						del games["{0}".format(ctx.message.channel.id)]
					else:
						embed = build_embed(ctx.message.author, ctx.message.channel.id, 0x00ff00)
						embed.add_field(name="Proposition:", value="{0}\nLettre présente !".format(arg.upper()),
						                inline=True)
						embed.add_field(name="Mot:", value=game.word.get_finded(), inline=True)
				elif test == False:
					embed = build_embed(ctx.message.author, ctx.message.channel.id, 0xff0000)
					embed.add_field(name="Proposition:", value="{0}\nLettre incorrecte...".format(arg.upper()),
					                inline=True)
					embed.add_field(name="Mot:", value=game.word.get_finded(), inline=True)
				elif test == "lost":
					embed = build_embed(ctx.message.author, ctx.message.channel.id, 0xff0000)
					embed.add_field(name="Proposition:",
					                value="{0}\nLettre incorrecte\nPartie perdue...".format(arg.upper()), inline=True)
					embed.add_field(name="Mot:", value=game.word.word, inline=True)
					del games["{0}".format(channel_id)]
			else:
				embed = build_embed(ctx.message.author, ctx.message.channel.id, 0xffff00)
				embed.add_field(name="Proposition:".format(arg),
				                value="{0}\nCaractère non pris en charge".format(arg), inline=True)
				embed.add_field(name="Mot:", value=game.word.get_finded(), inline=True)

		elif len(arg) != 1:
			test = game.try_word(arg)
			if test == True:
				embed = build_embed(ctx.message.author, ctx.message.channel.id, 0x00ff00)
				embed.add_field(name="Partie gagnée:", value="Bien joué !", inline=True)
				embed.add_field(name="Proposition:", value="{0}".format(arg), inline=True)
				del games["{0}".format(ctx.message.channel.id)]

			elif test == False:
				embed = build_embed(ctx.message.author, ctx.message.channel.id, 0xff0000)
				embed.add_field(name="Proposition:", value="{0}\nMot incorrect...".format(arg), inline=True)
				embed.add_field(name="Mot:", value=game.word.get_finded(), inline=True)
			elif test == "lost":
				embed = build_embed(ctx.message.author, ctx.message.channel.id, 0xff0000)
				embed.add_field(name="Proposition:".format(arg),
				                value="{0}\nMot incorrect\nPartie perdue...".format(arg), inline=True)
				embed.add_field(name="Mot:", value=game.word.word, inline=True)
				del games["{0}".format(ctx.message.channel.id)]

		await ctx.send(embed=embed)

	except:
		channel_id = ctx.message.channel.id
		await ctx.send(embed=get_not_ingame_embed(ctx.message.author, channel_id))

@p.error
async def p_error(ctx, error):
	try:
		game = games["{0}".format(ctx.message.channel.id)]
		embed = build_embed(ctx.message.author, ctx.message.channel.id, 0xffff00)
		embed.add_field(name="Veuillez préciser une lettre/un mot !", value="{0}p <mot/lettre>".format("!"), inline=True)
		embed.add_field(name="Mot:", value=game.word.get_finded(), inline=False)
		await ctx.send(embed=embed)
	except:
		channel_id = ctx.message.channel.id
		await ctx.send(embed=get_not_ingame_embed(ctx.message.author, channel_id))





@bot.command()
async def reveal(ctx):
	channel_id = ctx.message.channel.id
	try:
		game = games["{0}".format(channel_id)]
		game.used_lifes = 10
		embed = build_embed(ctx.message.author, ctx.message.channel.id, 0xff0000)
		embed.add_field(name="Partie terminée", value="Vous avez abandonné", inline=True)
		embed.add_field(name=" Mot:", value=game.word.word, inline=True)
		del  games["{0}".format(channel_id)]
		await ctx.send(embed=embed)
	except:
		channel_id = ctx.message.channel.id
		await ctx.send(embed=get_not_ingame_embed(ctx.message.author, channel_id))




@bot.command()
async def h(ctx):
	channel_id = ctx.message.channel.id
	await ctx.send(embed=get_help_embed(ctx.author, channel_id))


@bot.command()
async def aide(ctx):
	channel_id = ctx.message.channel.id
	await ctx.send(embed=get_help_embed(ctx.author, channel_id))




log("INFO", "Starting Bot...")
bot.run(TOKEN)