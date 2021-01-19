import datetime
from time import time
from datetime import date
from datetime import time

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