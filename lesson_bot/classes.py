import datetime
from time import time
from datetime import date
from datetime import time

class lesson_day:
    def __init__(self, date, lesson_count, lesson_time):
        self.date = date
        self.lesson_count = lesson_count
        self.lesson_time = lesson_time

    def __str__(self):
        word = 'занятия'
        if self.lesson_count == 1:
            word = 'занятие'
        if self.lesson_count == 0:
            word = 'занятий'    
        
        return f'{self.date.day}.{self.date.month}.{self.date.year}: {self.lesson_count} {word} ({self.lesson_time})'

    def __lt__(self, other):
        print(other)
        return self.date.day < other.date.day
    def __gt__(self, other):
        return self.date.day > other.date.day  