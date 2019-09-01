import json
from discord.ext import commands
from discord.ext.commands import Context as CommandContext, CommandError

config = json.load(open('files/config.json'))


class AdminError(CommandError):
    pass


def isadmin():
    def predicate(ctx: CommandContext):
        if str(ctx.author.id) in config['admins']:
            return True
        else:
            raise AdminError("You're not an admin!")
    return commands.check(predicate)
