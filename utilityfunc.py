import discord
import re
import datetime
from time import time
import config
from datetime import date
from datetime import time
from sortedcontainers import SortedList

from classes import lesson_day
from bot import get_message
from bot import get_channel

def to_message(lesson_month: SortedList):
    start = f'Занятие {lesson_month[0].date.month}.{lesson_month[0].date.year} (всего {len(lesson_month)}):'

    for lesson in lesson_month:
        start += '\n'
        start += str(lesson)

    return start    

def count_lessons(hours, minutes):
    minutes += hours * 60
    lessons = minutes/90
    lessons = round(lessons)
    return lessons

def get_day(data):
    data = re.search('(\d\d).(\d\d).(\d\d\d\d): (\d) заняти[яей] \((\d):(\d\d):(\d\d)\)', data)
    day = lesson_day(date(int(data[1]), int(data[2]), int(data[3])), int(data[4]), time(int(data[5]), int(data[6]), int(data[7])))
    return day


async def get_lessons(msg_id=config.main_post_id):
    lessons = []
    msg = await get_message(msg_id)
    data = msg.content.split('\n')
   # print(data)

    data_re = re.search('Lessons (\d\d).\d\d \(total (\d)\)', data[0])
    #print(data_re[0])
    #print(data_re[1])
    #print(data_re[2])
    if int(data_re[1]) != date.month:
        msg.channel.send(msg.content)
        d = date.strftime('%m.%y')
        msg.edit(f'Lessons {d} (total 0):')
    lessons_month = int(data_re[2])
    #for i in data[1]:
     #   lessons.append(get_day[i])
    return lessons    