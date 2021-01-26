import discord
import re
import datetime
from time import time
import config
from datetime import date
from datetime import time
from sortedcontainers import SortedList

from utilityfunc import *
from classes import *

intents = discord.Intents.all()

client = discord.Client(intents=intents)

date = date.today()
time_started = None
lesson_time = None
lessons_month = 0

def get_channel(channel_id):
    return client.get_guild(config.server_id).get_channel(channel_id)
    
async def get_message(msg_id):
    return await client.get_guild(config.server_id).get_channel(config.bot_channel).fetch_message(msg_id)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #if message.content.startswith('$hello'):
        #await message.channel.send('Hello!')
    #if message.content.startswith('!post'):
        #await message.channel.send(f'3')
    #if message.content.startswith('!clear'): 
        #msg = await get_message(config.main_post_id)
        #await msg.edit(content='Занятия 01.21 (всего 3)')
    if message.content.startswith('!add'):
        print(message.content) 
        data = re.search('!add (\d\d) (\d):(\d\d):(\d\d)', message.content)
        print(data)
        msg = await get_message(config.main_post_id)

        lessons = SortedList(get_lessons())

        lesson_count = await count_lessons(int(data[2]), int(data[3]))
        lesson_date = date(date.year, date.month, int(data[1]))
        lesson_time = time(int(data[2]), int(data[3]), int(data[4]))

        new_lesson = lesson_day(lesson_date, lesson_count, lesson_time)

        lessons.add(new_lesson)
        
        await msg.edit(content=msg.content + f'\n {int(data[1])}.{int(data[2])}: занятие {int(data[3])} минут')

@client.event
async def on_voice_state_update(member, before, after):
    global first_joined
    global second_joined
    global time_started
    global lesson_time

    if before.channel != after.channel and (after.channel == get_channel(config.lesson_channel) or before.channel == get_channel(config.lesson_channel)):
        channel = get_channel(config.lesson_channel)
        if len(channel.members) >= 2:
            if time_started is None: time_started = time()
        elif time_started is not None:
            lesson_time = time() - time_started
            lesson_count = 0
            time_started = None
            d = date.strftime('%d.%m.%y')
            msg = await get_message(config.main_post_id)
            await msg.edit(content=msg.content + f'\n {d}: занятие {lesson_time/60:.2f} минут')

client.run(config.bot_id)