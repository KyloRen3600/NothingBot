from NothingAPI.core import log
import discord
import datetime
try:
	from Python.Discord.NothingBot.addons import get_addons_list
except:
	from Addon import get_addons_list

def build_embed(title, color):
	embed = discord.Embed(title=title,
	                      url="https://nothinggames.tk",
	                      color=color, timestamp=datetime.datetime.utcnow())
	embed.set_footer(text="Créé par NothingGames")
	return embed

def __main__(bot, addon):
	addon_list = get_addons_list(bot)

	@bot.command(aliases=["help", "aide", "commands", "commandes"])
	async def help_command(ctx):
		embed = build_embed("[Aide]", 0x1d9ca3)
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
		commands = ["- !addon <addon>: infos sur un Addon"]
		for script in addon_list:
			script = addon_list[script]
			if script.enabled:
				if script.commands:
					commands.append("- {0}: {1}".format(script.help_command, script.help_description))
		commands = "\n".join(commands)
		embed.add_field(name="Listes des commandes:",
		                value=commands)
		embed.set_thumbnail(url="http://tpeminicentralehydraulique.e-monsite.com/medias/images/la-rotation-des-engrenages-318-56336.jpg")
		await ctx.send(embed=embed)

	@bot.command(aliases=["addon", "addon_info", "Addon"])
	async def addon_infos(ctx):
		message = ctx.message.content
		args = message.split(" ")
		if len(args) == 1:
			embed = build_embed("[Erreur]", 0xff0000)
			embed.add_field(name="Veuillez spécifier un addon !",
			                value="!addon list pour connaître la liste des addons", inline=True)
		else:
			del args[0]
			if args[0] == "list":
				embed = build_embed("Liste des Addons:", 0x1d9ca3)
				for addon in addon_list:
					addon = addon_list[addon]
					if addon.enabled:
						name = F"{addon.name}:"
						if addon.commands:
							embed.add_field(name=name, value="{0}\n{1}".format(addon.description, addon.help_command), inline=False)
						else:
							embed.add_field(name=name, value=addon.description, inline=False)

			else:
				try:
					addon = addon_list[" ".join(args).lower()]
				except:
					addon = "erreur"
				if addon != "erreur":
					embed = build_embed("[{0}]".format(addon.name), 0x1d9ca3)
					embed.add_field(name="Description:", value=addon.description, inline=True)
					embed.add_field(name="Version:", value=addon.version, inline=True)
					embed.add_field(name="Commande d'aide:", value=addon.help_command, inline=True)
					embed.add_field(name="Développeur:", value=addon.developer, inline=True)
					embed.set_thumbnail(url="https://github.com/KyloRen3600/KyloBot-Addons/blob/master/src/Icons/PFC.png?raw=true")
				else:
					embed = build_embed("[Erreur]", 0xff0000)
					embed.add_field(name="Addon invalide !", value="!addon list pour connaître la liste des addons", inline=True)
		await ctx.send(embed=embed)