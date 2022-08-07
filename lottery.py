#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 10:48:08 2022

@author: julianhamre
"""

from timeit import default_timer as dt
from random import randint
import sys
import getopt

def one_equal_number(number, numbers):
    for i in numbers:
        if i == number:
            return True
    return False

def random_lottery_numbers():
    numbers = []
    while len(numbers) < 7:
        number = randint(1, 35)  # fix range issue
        if not one_equal_number(number, numbers):
            numbers.append(number)  
    numbers.sort()
    return numbers

def play_lottery_until_won():
    win = random_lottery_numbers()
    play = random_lottery_numbers()
    counter = 1
    while not win == play:
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


class commands:
    __passed_arguments = sys.argv[1:]
    
    def execute_single_options(self):
        flags = "np"
        full_opts = "numbers", "play", "number_sets="
        opts, args = getopt.getopt(self.__passed_arguments, flags, full_opts)
    
        for opt, arg in opts:
            if opt in ["-n"] or opt in ["--numbers"]:
                print(random_lottery_numbers())
            if opt in ["--number_sets"]:
                for i in range(int(arg)):
                    print(f"list {i+1}:", random_lottery_numbers())
            if opt in ["-p"] or opt in ["--play"]:
                attempt = play_lottery_until_won()
                print("won in attempt number", attempt)
                

cm = commands()
cm.execute_single_options()