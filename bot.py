import discord
from datetime import datetime
from discord.ext import commands


bot = commands.Bot(command_prefix= '$')
delete_delay = 3600


# ModCommands
@bot.command()
@commands.has_role('Mod')
async def set_delete_delay(ctx, delay : int):
    global delete_delay
    delete_delay = delay
    print('New delay for logging deletion: {0}s'.format(delay))
    await ctx.message.delete()

@bot.command()
@commands.has_role('Mod')
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount+1)

@bot.command()
@commands.has_role('Mod')
async def shutdown(ctx):
    await ctx.bot.logout()


#Commands

# Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.message.delete()
        await ctx.send('Fehlende Berechtigung für diesen Command!', delete_after=10)


# Logging events
@bot.event
async def on_voice_state_update(member, before, after):
    log_channel = bot.get_channel(807378072947916800)
    if before.channel is None and after.channel is not None:
        
        print('{0.name} joined {1.name} ({1.id})'.format(member, after.channel))
        
        if after.channel.id != 807381763914465291:
            timestamp = await get_timestamp()
            await send_logging_info(log_channel, member, '[{0}]: {1.name} joined {2.name}'.format(timestamp, member, after.channel), delete_delay)
        
    if before.channel is not None and before.channel is not after.channel and after.channel is not None:
        
        print('{0.name} left {1.name}'.format(member, before.channel))
        print('{0.name} joined {1.name}'.format(member, after.channel))

        if after.channel.id != 807381763914465291 and before.channel.id != 807381763914465291:
            timestamp = await get_timestamp()
            await send_logging_info(log_channel, member, '[{0}]: {1.name} went from {2.name} to {3.name}'.format(timestamp, member, before.channel, after.channel), delete_delay)

    if before.channel is not None and after.channel is None:
        
        print('{0.name} left {1.name}'.format(member, before.channel))

        if before.channel.id != 807381763914465291:
            timestamp = await get_timestamp()
            await send_logging_info(log_channel, member, '[{0}]: {1.name} left {2.name}'.format(timestamp, member, before.channel), delete_delay)


# Helper methods
async def get_timestamp():
    now = datetime.now()
    date_time = now.strftime("%d.%m.%Y %H:%M:%S")
    return date_time

async def send_logging_info(channel, member, text, delete_delay):
    
    embed = discord.Embed()
    embed.set_author(name = text, icon_url = member.avatar_url)
    await channel.send(embed=embed, delete_after=delete_delay)


# Stuff
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

bot.run('')