#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 10:48:08 2022

@author: julianhamre
"""

from timeit import default_timer as dt
from random import randint

def equal_number(number, numbers):
    for i in numbers:
        if i == number:
            return True
    return False
    

def random_lottery_numbers():
    numbers = []
    while len(numbers) < 7:
            number = randint(1, 35)
            if not equal_number(number, numbers):
                numbers.append(number)  
    return numbers


def numbers_compare(lottery_numbers, random_numbers):
    for i in lottery_numbers:
        if not equal_number(i, random_numbers):
            return False
    return True


def play_lottery_until_won():
    win = random_lottery_numbers()
    play = random_lottery_numbers()
    counter = 1
    while not numbers_compare(win, play):
        play = random_lottery_numbers()
        counter += 1
        if counter % 100000 == 0:
            print(f"{counter / 1000000} million attempts")
    return counter



start = dt()

print("won in attempt number", play_lottery_until_won())

end = dt()

print(f"run in {round(end - start, 4)} seconds")
