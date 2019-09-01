# Importing some important stuffs
from discord import Message
from discord.ext import commands
from files import colors
from os import listdir
from shutil import copyfile
from json import loads

config = {}


if 'config.json' not in listdir('files'):
    print(f'{colors.RED}ERROR: Config file not found! Creating it...{colors.END}')
    copyfile('files/config.json.EXAMPLE', 'files/config.json')
    quit(404)
else:
    config = loads(open('files/config.json').read())


# Getting the server-specific prefix
def get_server_prefix(bot: commands.Bot, message: Message):
    if not message.guild:
        return config["prefix"]
    prefix = config["prefix"]
    return commands.when_mentioned_or(prefix)(bot, message)


# Setting up our bot-client
client: commands.bot = commands.AutoShardedBot(command_prefix=get_server_prefix)

# Listing all module-files in the /modules folder
MODULES = []
for i in listdir("modules"):
    if i.endswith('.py'):
        MODULES.append('modules.' + i[:-3])
    else:
        continue

# Importing the previously listed commands
print("--"*20)
print(f"{colors.YELLOW}LOADING MODULES!{colors.END}")
print("--"*20)
for module in MODULES:
    try:
        client.load_extension(module)
        print(f"{colors.CYAN}Module {module}{colors.END}: {colors.GREEN}LOADED{colors.END}")
    except Exception as e:
        print(f"{colors.CYAN}Module {module}{colors.END}: {colors.RED}NOT LOADED\n({e}){colors.END}")
print("--"*20)

# Running the bot
if __name__ == "__main__":
    client.run(config["bot-token"])
