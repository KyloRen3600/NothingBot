from NothingAPI import log
import discord
import asyncio




def __main__(bot, addon):
    async def search_submissions():
        await bot.wait_until_ready()
        run = 0
        while True:
            run += 1
            await bot.change_presence(activity=discord.Streaming(name=run,
                                                                 url="https://twitch.tv/NothingBot", type=1))
            log("Ok", "Status updated")
            await asyncio.sleep(1)
    log(addon.name, "Status Updater loaded !")
    bot.loop.create_task(search_submissions())


