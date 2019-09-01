import checks
from discord import Embed, Colour, FFmpegPCMAudio
from discord.ext import commands
from discord.ext.commands import Context as CommandContext, Cog
from files import colors
from os import listdir, mkdir, remove
from os.path import exists
from asyncio import sleep
from mutagen.mp3 import MP3
from mutagen.wavpack import WavPack
from mutagen.ogg import OggFileType

ffmpeg_options = {
    'options': '-vn'
}

voice_clients = {

}


class SoundBoardCog(Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command()
    @checks.isadmin()
    async def add_sound(self, ctx: CommandContext, name: str = None):
        if ctx.message.attachments:
            addable = [ctx.message.attachments[0].filename for x in ['.mp3', '.ogg', '.wav'] if x in ctx.message.attachments[0].filename]
            if addable:
                if name:
                    msg = await ctx.send(embed=Embed(
                        title="Adding sound!",
                        description="Downloading...",
                        color=Colour.gold()
                    ))
                    await ctx.message.attachments[0].save('sounds/{}.{}'.format(name, ctx.message.attachments[0].filename.split('.')[1]))
                    await msg.edit(embed=Embed(
                        title="Sound added",
                        description="Added sound as: **{}**".format(name),
                        color=Colour.green()
                    ))
                else:
                    msg = await ctx.send(embed=Embed(
                        title="Adding sound!",
                        description="Downloading...",
                        color=Colour.gold()
                    ))
                    await ctx.message.attachments[0].save('sounds/{}'.format(ctx.message.attachments[0].filename))
                    await msg.edit(embed=Embed(
                        title="Sound added",
                        description="Added sound as: **{}**".format(ctx.message.attachments[0].filename[:-4]),
                        color=Colour.green()
                    ))
            else:
                await ctx.send(embed=Embed(
                    title="Error",
                    description="File type needs to be either **.mp3 .wav or .ogg**!",
                    color=Colour.red()
                ))
        else:
            await ctx.send(embed=Embed(
                title="Error",
                description="You need to send a file and put the command as its comment!",
                color=Colour.red()
            ))

    @commands.command()
    @checks.isadmin()
    async def remove_sound(self, ctx: CommandContext, sound: str = None):
        if not sound:
            await ctx.send(embed=Embed(
                title="Error",
                description="You need to specify which sound to remove!",
                color=Colour.red()
            ))
        else:
            to_remove = None
            for i in listdir('sounds'):
                if i.lower().startswith(sound.lower()):
                    to_remove = 'sounds/' + i
                    break
            if to_remove:
                remove(to_remove)
                await ctx.send(embed=Embed(
                    title="Sound removed!",
                    description=f"Deleted file: **{to_remove}**!",
                    color=Colour.green()
                ))
            else:
                await ctx.send(embed=Embed(
                    title="Error",
                    description=f"There's no sound that starts with/is named **{sound}**!\nTry **{ctx.prefix}sounds** for a list of sounds!",
                    color=Colour.red()
                ))

    @commands.command()
    async def sounds(self, ctx: CommandContext):
        desc = '\r'.join([x[:-4] for x in listdir('sounds')])
        await ctx.send(embed=Embed(
            title="Sounds",
            description=f"```fix\nAll available sounds are=\n{desc}```",
            color=Colour.blurple()
        ))

    @commands.command()
    async def play(self, ctx: CommandContext, sound: str = None):

        async def after(guild_id, length):
            await sleep(length)
            try:
                await voice_clients[str(guild_id)].disconnect()
                voice_clients[str(guild_id)] = None
            except:
                pass

        if not ctx.author.voice:
            await ctx.send(embed=Embed(
                title="Error",
                description="You need to be in a voice channel to summon me!",
                color=Colour.red()
            ))
            return
        if sound:
            to_play = None
            for i in listdir('sounds'):
                if i.lower().startswith(sound.lower()):
                    to_play = 'sounds/' + i
                    break
            if to_play:
                try:
                    if to_play.endswith('.mp3'):
                        length = MP3(to_play).info.length
                    elif to_play.endswith('.ogg'):
                        length = OggFileType(to_play).info.length
                    else:
                        length = WavPack(to_play).info.length
                    client = await ctx.author.voice.channel.connect()
                    src = FFmpegPCMAudio(to_play, options=ffmpeg_options)
                    client.play(src)
                    voice_clients[str(ctx.guild.id)] = client
                    await after(ctx.guild.id, length)
                except:
                    await ctx.send(embed=Embed(
                        title="Error",
                        description="Couldn't join your channel! Maybe I'm missing permissions?",
                        color=Colour.red()
                    ))
            else:
                await ctx.send(embed=Embed(
                    title="Error",
                    description=f"Sound **{sound}** not found! Use **{ctx.prefix}sounds** for a list of sounds!",
                    color=Colour.red()
                ))
        else:
            await ctx.send(embed=Embed(
                title="Error",
                description=f"You need to specify a sound! Use **{ctx.prefix}sounds** for a list of sounds!",
                color=Colour.red()
            ))

    @commands.command()
    async def stop(self, ctx: CommandContext):
        if str(ctx.guild.id) in voice_clients:
            if voice_clients[str(ctx.guild.id)]:
                if ctx.author in voice_clients[str(ctx.guild.id)].channel.members:
                    await voice_clients[str(ctx.guild.id)].disconnect()
                    await ctx.send(embed=Embed(
                        title="Stopping playback!",
                        description=f"Disconnecting from {voice_clients[str(ctx.guild.id)].channel.name}!",
                        color=Colour.green()
                    ))
                    voice_clients[str(ctx.guild.id)] = None
                else:
                    await ctx.send(embed=Embed(
                        title="Error",
                        description="You need to be in a channel with the bot!",
                        color=Colour.red()
                    ))
            else:
                await ctx.send(embed=Embed(
                    title="Error",
                    description="There apparently isn't a sound being played on this server!",
                    color=Colour.red()
                ))
        else:
            await ctx.send(embed=Embed(
                title="Error",
                description="There apparently isn't a sound being played on this server!",
                color=Colour.red()
            ))


def setup(bot: commands.Bot):
    if not exists('sounds'):
        mkdir('sounds')
        print(f'{colors.YELLOW}WARN: Folder {colors.CYAN}/sounds{colors.YELLOW} not found! Creating it now!{colors.END}')
    bot.add_cog(SoundBoardCog(bot))
