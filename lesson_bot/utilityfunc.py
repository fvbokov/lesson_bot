import discord
import re
import datetime
from time import time
from datetime import date
from datetime import time
from sortedcontainers import SortedList

from .classes import lesson_day


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
    data = re.search('(\d\d).(\d\d).(\d\d\d\d): (\d) lessons? \((\d):(\d\d):(\d\d)\)', data)
    #print(f"date({int(data[1])}, {int(data[2])}, {int(data[3])})")
    day = lesson_day(date(int(data[3]), int(data[2]), int(data[1])), int(data[4]), time(int(data[5]), int(data[6]), int(data[7])))
    return day


def get_lessons(message):
    lessons = []
    data = message.split('\n')

    for i in data[2:]:
        lessons.append(get_day(i))
    
    return lessons