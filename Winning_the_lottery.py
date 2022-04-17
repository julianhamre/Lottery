#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 10:48:08 2022

@author: julianhamre
"""

from timeit import default_timer as dt
from random import randint

def one_equal_number(number, numbers):
    for i in numbers:
        if i == number:
            return True
    return False
    

def all_equal_numbers(numbers1, numbers2):
    for i in numbers1:
        if not one_equal_number(i, numbers2):
            return False
    return True


def random_lottery_numbers():
    numbers = []
    while len(numbers) < 7:
            number = randint(1, 35)
            if not one_equal_number(number, numbers):
                numbers.append(number)  
    return numbers


def play_lottery_until_won():
    win = random_lottery_numbers()
    play = random_lottery_numbers()
    counter = 1
    while not all_equal_numbers(win, play):
        play = random_lottery_numbers()
        counter += 1
        if counter % 100000 == 0:
            print(f"{counter / 1000000} million attempts")
    return counter


def attempts_append_to_txt():
    counter = 1
    for i in range(0, 100):
        f = open("lottery_winning_attempts.txt", "a") 
        f.write(f"{play_lottery_until_won()}\n")
        print(counter, "elements added to lottery_winning_attempts")
        f.close()
        counter += 1


def average_attempt():
    average = 0
    with open("lottery_winning_attempts.txt") as f:
        lines = f.readlines()
        for line in lines:
            average += int(line)
        average /= len(lines)
    return average
        

start = dt()

print("won in attempt number", play_lottery_until_won())
#attempts_append_txt()
#print(average_attempt())

end = dt()

print(f"run in {round(end - start, 4)} seconds")


