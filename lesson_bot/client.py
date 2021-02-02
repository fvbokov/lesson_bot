import re
import datetime
import time
import discord
from sortedcontainers import SortedList

from .classes import lesson_day
from .config import server_id, bot_channel, lesson_channel, main_post_id
from .utilityfunc import get_lessons, count_lessons


class Client(discord.Client):
    def __init__(self, *a, **kwa):
        for arg in a:
            print(arg)
        
        for k in kwa:
            print(f"{k}: {kwa[k]}")
        
        super().__init__(*a, **kwa)
        
        self.time_started = None

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_message(self, message):
        if message.author == self.user:
            return

        #if message.content.startswith('$hello'):
            #await message.channel.send('Hello!')
        if message.content.startswith('!post'):
            await message.channel.send('Lessons 01.21 (total 7):\n\n05.01.2021: 1 lesson (1:45:22)')
        #if message.content.startswith('!clear'): 
            #msg = await self.get_guild(server_id).get_channel(bot_channel).fetch_message(main_post_id)
            #await msg.edit(content='Занятия 01.21 (всего 3)')
        if message.content.startswith('!add'):
            print(message.content) 
            data = re.search('!add (\d\d) (\d):(\d\d):(\d\d)', message.content)
            msg = await self.get_guild(server_id).get_channel(bot_channel).fetch_message(main_post_id)
            today = datetime.date.today()

            msg_data = msg.content.split('\n')
            msg_data_re = re.search('Lessons (\d\d).\d\d \(total (\d)\)', msg_data[0])
            if int(msg_data_re[1]) != today.month:
                msg.channel.send(msg.content)
                d = today.strftime('%m.%y')
                msg.edit(f'Lessons {d} (total 0):')

            lessons = SortedList(get_lessons(msg.content))

            lesson_count = count_lessons(int(data[2]), int(data[3]))
            lesson_date = datetime.date(today.year, today.month, int(data[1]))
            lesson_time = datetime.time(int(data[2]), int(data[3]), int(data[4]))

            new_lesson = lesson_day(lesson_date, lesson_count, lesson_time)

            lessons.add(new_lesson)
            
            await msg.edit(content=msg.content + f'\n {int(data[1])}.{int(data[2])}: занятие {int(data[3])} минут')

    async def on_voice_state_update(self, member, before, after):
        channel = self.get_guild(server_id).get_channel(lesson_channel)

        if before.channel != after.channel and (after.channel == channel or before.channel == channel):
            if len(channel.members) >= 2:
                if time_started is None: time_started = time.time()
            elif time_started is not None:
                lesson_time = time.time() - time_started
                time_started = None
                d = datetime.date.today().strftime('%d.%m.%y')
                msg = await self.get_guild(server_id).get_channel(bot_channel).fetch_message(main_post_id)
                await msg.edit(content=msg.content + f'\n {d}: занятие {lesson_time/60:.2f} минут')
