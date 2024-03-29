from files import colors
from checks import AdminError
from discord import opus, Embed, Colour
from discord.ext import commands
from discord.ext.commands import Context as CommandContext, Cog


class SystemCog(Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f"{colors.YELLOW}BOT STARTED!{colors.END}")
        print("--" * 20)
        print(f"{colors.CYAN}Name{colors.END}: {colors.YELLOW}{self.bot.user.name}{colors.END}")
        print(f"{colors.CYAN}ID{colors.END}: {colors.YELLOW}{self.bot.user.id}{colors.END}")
        print(f"{colors.CYAN}Guilds{colors.END}: {colors.YELLOW}{len(self.bot.guilds)}{colors.END}")
        print("--" * 20)
        print(f"{colors.CYAN}Invite{colors.END}: https://www.discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=-1")
        print("--" * 20)
        if opus.is_loaded():
            print(f"{colors.CYAN}Opus is loaded and ready!{colors.END}")
            print("--" * 20)

    @Cog.listener()
    async def on_command_error(self, ctx: CommandContext, exc: BaseException):
        if isinstance(exc, AdminError):
            await ctx.send(embed=Embed(
                title="Error",
                description="You need to be an admin to run this command!",
                color=Colour.red()
            ))


def setup(bot: commands.Bot):
    bot.add_cog(SystemCog(bot))
