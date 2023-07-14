from mcstatus import JavaServer
import discord
import asyncio
import datetime
import json_database

bot = discord.Bot()
data = json_database.getdata()

offset = datetime.timedelta(hours=data['timezone_offset'])
tzinfo = datetime.timezone(offset, name='МСК')

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await update_status()


async def update_status():
    while True:
        print('cycle')
        server = JavaServer.lookup(data['ip'])
        try:
            status = server.status()
            print(status)
            if status.players.max == 0:
                online = False
            else:
                online = True
                desc = f'Онлайн | {status.players.online}/{status.players.max} игроков'
        except Exception as e:
            online = False
            print('exception', e)
        embed = discord.Embed(title=data['ip'], description=desc if online else 'Офлайн', color=data['embed_color'])
        ts = datetime.datetime.now(tz=tzinfo).time().strftime('%H:%M')
        embed.set_footer(text=' Обновленоᅠ•ᅠCегодня в ' + ts)
        channel = bot.get_channel(data['channel_id'])
        if not data['message_id']:
            message = await channel.send(embed=embed)
            data['message_id'] = message.id
            json_database.senddata(data)
        else:
            await channel.get_partial_message(data['message_id']).edit(embed=embed)
        await asyncio.sleep(data['time'])


def startup():
    return bot.run(token=data['token'])


startup()
