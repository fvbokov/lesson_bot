import discord
import re
import datetime
from time import time
import config
from datetime import date
from datetime import time

intents = discord.Intents.all()

client = discord.Client(intents=intents)

date = date.today()
time_started = None
lesson_time = None
lessons_month = 0

class lesson_month:
    lessons = []

    def __init__(self, lessons):
        self.lessons = lessons

    def sort(self):
        for i in range(1, len(self.lessons)):
            el = self.lessons[i]
            j = i
            while j > 0 and self.lessons[j - 1] > el:
                self.lessons[j] = self.lessons[j - 1]
                j -= 1
            self.lessons[j] = el

    def insert(self, lesson_day):
        self.lessons.append(lesson_day)
        self.sort()

class lesson_day:
    def __init__(self, date, lesson_count, lesson_time):
        self.date = date
        self.lesson_count = lesson_count
        self.lesson_time = time

    def __str__(self):
        word = 'занятия'
        if lesson_count == 1:
            word = 'занятие'
        if lesson_count == 0:
            word = 'занятий'    
        
        return f'{self.date.day}.{self.date.month}.{self.date.year}: {self.lesson_count} {word} ({self.lesson_time})'

    def __lt__(self, other):
        return self.date.day < other.date.day
    def __gt__(self, other):
        return self.date.day > other.date.day      

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

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('!post'):
        await message.channel.send(f'3')
    if message.content.startswith('!clear'): 
        msg = await get_message(config.main_post_id)
        await msg.edit(content='Занятия 01.21 (всего 3)')
    if message.content.startswith('!add'): 

        data = re.search('^!add (\d\d) (\d):(\d\d):(\d\d)', message.content)
        msg = await get_message(config.main_post_id)
        lessons = lesson_month(get_lessons())
        
        new_lesson = lesson_day

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