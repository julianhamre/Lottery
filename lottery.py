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
        number = randint(1, 34)
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
            print(f"{counter / 1000000} million attempts", end="\r")
    return counter

def attempt_append_to_txt(winning_attempt, file_name):
    f = open(file_name, "a") 
    f.write(f"{winning_attempt}\n")
    f.close()

def average_attempt(file_name):
    average = 0
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            average += int(line)
        average /= len(lines)
    return average


class commands:
    __passed_arguments = sys.argv[1:]
    
    def __single_options(self):
        flags = "nN:A:"
        full_opts = "numbers", "number_sets=", "average_attempt="
        opts, args = getopt.getopt(self.__passed_arguments, flags, full_opts)
    
        for opt, arg in opts:
            if opt in ["-n"] or opt in ["--numbers"]:
                print(random_lottery_numbers())
            if opt in ["-N"] or opt in["--number_sets"]:
                for i in range(int(arg)):
                    print(f"set {i+1}:", random_lottery_numbers())
            if opt in ["-A"] or opt in ["--average_attempt"]:
                print("average:", round(average_attempt(arg), 2))
                
      
    def __play_options(self):
        arguments = self.__passed_arguments[1:]
        flags = "a:t:"
        full_opts = "append_winning_attempt=", "times="
        opts, args = getopt.getopt(arguments, flags, full_opts)
        times = 1
        
        for opt, arg in opts:
            if opt in ["-t"] or opt in ["--times"]:
                times = int(arg)
        
        append = False
        
        for opt, arg in opts:
            if opt in ["-a"] or opt in ["--append_winning_attempt"]:
                append = True
                file_name = arg
        
        for i in range(times):
            winning_attempt = play_lottery_until_won()
            loop_count = f"{i+1}/{times},"
            if append:
                attempt_append_to_txt(winning_attempt, file_name)
                print(loop_count, "appended winning attempt", winning_attempt)
            else:
                print(loop_count, "won in attempt", winning_attempt)
        
        
    def execute(self):
        if self.__passed_arguments[0] == "play":
            self.__play_options()
        else:
            self.__single_options()
    

cm = commands()
cm.execute()