import NothingAPI

def __main__(client, addon):
    NothingAPI.log(addon.name, "Thanks for using PFC !")
    @client.command()
    async def p(ctx):
        NothingAPI.log("info", "command invoked")

    @client.command()
    async def a(ctx):
        NothingAPI.log("info", "foinffji")
