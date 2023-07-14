from mcstatus import JavaServer
import discord
import asyncio
import datetime
import json_database

bot = discord.Bot()
data = json_database.getdata()

offset = datetime.timedelta(hours=data['timezone_offset'])
tzinfo = datetime.timezone(offset, name='МСК')

previous_players = []


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
            if status.players.sample:
                names = [i.name for i in status.players.sample]
            else:
                names = []
            if status.players.max == 0:
                online = False
                names = []
            else:
                online = True
                desc = f'Онлайн | {status.players.online}/{status.players.max} игроков'
        except Exception as e:
            names = []
            online = False
            print('exception', e)

        log_channel = bot.get_channel(data['log_channel_id'])
        print(names)
        for old_player in previous_players:
            if old_player not in names:
                await log_channel.send(content=f'{old_player} вышел с сервера')
        for new_player in names:
            if new_player not in previous_players:
                await log_channel.send(content=f'{new_player} зашел на сервер')
        previous_players.clear()
        previous_players.extend(names)

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
