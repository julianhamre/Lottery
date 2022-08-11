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


def random_lottery_numbers():
    numbers = []
    while len(numbers) < 7:
        number = randint(1, 34)
        if not number in numbers:
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


class bcolors:
    red = "\u001b[31m"
    green = "\u001b[32m"


class equal_numbers:

    def __init__(self, number_set, number_sets_file_name):
        self.__input_set = number_set
        self.__number_sets_file = number_sets_file_name
        self.__search = False
    
    def __set_search_bool(self, string):
        if "[" in string:
            self.__search = True
        if "]" in string:
            self.__search = False
    
    def __strip_string_number(self, str_numb):
        if "[" in str_numb:
            str_numb = str_numb.replace("[", "")
        if "," in str_numb:
            str_numb = str_numb.replace(",", "")
        if "]" in str_numb:
            str_numb = str_numb.replace("]", "")
        return str_numb
        
    def detect(self):
        with open(self.__number_sets_file) as f:
            all_equals = []
            for line in f.readlines():
                line_equals = []
                for str_numb in line.split():
                    self.__set_search_bool(str_numb)
                    if self.__search:
                        for numb in self.__input_set:
                            file_numb = int(self.__strip_string_number(str_numb))
                            if numb == file_numb:
                                line_equals.append(numb)
                all_equals.append(line_equals)
        return all_equals


class single_options:
    
    def __init__(self, arguments):
        self.__arguments = arguments
    
    def execute(self):
        flags = "nN:A:"
        full_opts = "numbers", "number_sets=", "average_attempt="
        opts, args = getopt.getopt(self.__arguments, flags, full_opts)
    
        for opt, arg in opts:
            if opt in ["-n"] or opt in ["--numbers"]:
                print(random_lottery_numbers())
            if opt in ["-N"] or opt in["--number_sets"]:
                for i in range(int(arg)):
                    print(f"set {i+1}:", random_lottery_numbers())
            if opt in ["-A"] or opt in ["--average_attempt"]:
                print("average:", round(average_attempt(arg), 2))
                

class play_options:

    def __init__(self, arguments):
        arguments = arguments[1:]
        flags = "a:t:"
        full_string_opts = "append_winning_attempt=", "times="
        opts, args = getopt.getopt(arguments, flags, full_string_opts)
        
        self.__times = 1
        self.__append = False
        
        for opt, arg in opts:
            if opt in ["-t"] or opt in ["--times"]:
                self.__times = int(arg)
            if opt in ["-a"] or opt in ["--append_winning_attempt"]:
                self.__append = True
                self.__file_name = arg
        

    def execute(self):    
        for i in range(self.__times):
            winning_attempt = play_lottery_until_won()
            loop_count = f"{i+1}/{self.__times},"
            if self.__append:
                attempt_append_to_txt(winning_attempt, self.__file_name)
                print(loop_count, "appended winning attempt", winning_attempt)
            else:
                print(loop_count, "won in attempt", winning_attempt)
        
        
def execute_commands():
    arguments = sys.argv[1:]
    if arguments[0] == "play":
        play_options(arguments).execute()
    else:
        single_options(arguments).execute()

if len(sys.argv) > 1:
    execute_commands()