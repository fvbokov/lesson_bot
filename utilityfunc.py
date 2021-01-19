import discord
import re
import datetime
from time import time
import config
from datetime import date
from datetime import time

from .classes import lesson_month
from .classes import lesson_day

def get_channel(channel_id):
    return client.get_guild(config.server_id).get_channel(channel_id)
    
async def get_message(msg_id):
    return await client.get_guild(config.server_id).get_channel(config.bot_channel).fetch_message(msg_id)

def get_day(data):
    data = re.search('(\d\d).(\d\d).(\d\d\d\d): (\d) заняти[яей] \((\d):(\d\d):(\d\d)\)', data)
    day = lesson_day(date(int(data[1]), int(data[2]), int(data[3])), int(data[4]), time(int(data[5]), int(data[6]), int(data[7])))
    return day

async def get_lessons(msg_id=config.main_post_id):
    lessons = []
    msg = await get_message(msg_id)
    data = msg.content
    data = data.split('\n')

    data[0] = re.search('^Занятия (\d\d).\d\d\d\d \(всего (\d+)\):', data[0])
    if int(data[0][1]) != date.month:
        msg.channel.send(msg.content)
        d = date.strftime('%m.%y')
        msg.edit(f'Занятия {d} (всего 0):')
    lessons_month = int(data[0][2])
    data.pop(1)
    for i in data[1:]:
        lessons.append(get_day[i])
    return lessons    