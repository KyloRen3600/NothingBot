import pafy
from NothingAPI.core import log
import discord
import datetime

def build_embed(title, color, url=None):
	embed = discord.Embed(title=title,
						  url=url,
						  color=color, timestamp=datetime.datetime.utcnow())
	embed.set_footer(text="Développé par NothingGames")
	return embed
def __main__(client, addon):
	log(addon.name, "YouTube Downloader loaded !")
	@client.command()
	async def youtube(ctx):
		message = ctx.message.content
		args = message.split(" ")
		if len(args) == 1:
			embed = build_embed("Erreur", color=0x1d9ca3)
		else:
			log("info", "command invoked")
			video = pafy.new(args[1])
			best_url = video.getbest().url
			video_url = video.getbestvideo().url
			audio_url = video.getbestaudio().url


			embed = build_embed(video.title, url=args[1], color=0x1d9ca3)
			embed.set_thumbnail(url=video.bigthumb)
			embed.add_field(name="Vidéo et Audio:", value=F"[Vidéo et Audio]({best_url})", inline=False)
			embed.add_field(name="Vidéo", value=F"[Vidéo]({video_url})", inline=False)
			embed.add_field(name="Audio", value=F"[Audio]({audio_url})", inline=False)
		await ctx.send(embed=embed)


