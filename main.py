# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import os
import random

import discord
from discord.ext import commands
from pathlib import Path
from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# client = discord.Client()
intents = discord.Intents().all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')

sink = discord.sinks.WaveSink()


@client.event
async def on_ready():
    print('im ready')


@client.command()
async def cut(ctx):
    await ctx.invoke(client.get_command('stop'))
    global sink
    sink = discord.sinks.WaveSink()
    await ctx.invoke(client.get_command('rec'))
    return


@client.command()
async def join(ctx: commands.Context):
    channel: discord.VoiceChannel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect()
    await ctx.invoke(client.get_command('rec'))


@client.command()
async def test(ctx):
    await ctx.send('hello im alive!')


@client.command()
async def rec(ctx):
    ctx.voice_client.start_recording(sink=sink, callback=write_from_sink)
    embedVar = discord.Embed(title="Started the Recording!",
                             description="use !stop to stop!", color=0x546e7a)
    await ctx.send(embed=embedVar)


@client.command()
async def stop(ctx: commands.Context):
    await ctx.send(f'Stopping the Recording')

    try:
        ctx.voice_client.stop_recording()
    except discord.sinks.RecordingException:
        return

@client.command()
async def loop(ctx: commands.Context):
    loopcut.start(ctx)

@client.command()
async def stoploop(ctx: commands.Context):
    loopcut.start(ctx)


@client.command()
async def disconnect(ctx: commands.Context):
    await ctx.voice_client.disconnect()

@rec.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError(
                "Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()


@tasks.loop(minutes=2)
async def loopcut(ctx):
    await ctx.invoke(client.get_command('stop'))
    global sink
    print('loopa')
    sink = discord.sinks.WaveSink()
    await ctx.invoke(client.get_command('rec'))

async def write_from_sink(args):
    for audio in args.audio_data:
        if args.audio_data[audio].finished:
            user = await client.fetch_user(audio)
            try:
                os.mkdir(user.name + '/')
            except FileExistsError:
                pass
            if not os.path.exists(Path(os.getcwd() + fr"\{user.name}\lastnum")):
                lastnum = 0
            else:
                with open(Path(os.getcwd() + fr'\{user.name}\lastnum'), "r") as f:
                    s = f.read()
                    lastnum = int(s)
                    lastnum += 1
                    f.close()
            with open(Path(os.getcwd() + "/" + user.name + '/' + str(lastnum) + '.wav'), "wb") as f:
                f.write(args.audio_data[audio].file.getbuffer())
                f.close()
            with open(Path(os.getcwd() + fr'\{user.name}\lastnum'), "w") as f:
                f.write(f"{lastnum}")
                f.close()
    global sink
    sink = discord.sinks.WaveSink()



client.run(token)

try:
    client.run(token)
except:
    os.system("kill 1")
