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
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class separated_numbers:
    
    def __init__(self):
        self.__main = ""
        self.__line_count = 1
        
    def new_line(self):
        self.end()
        self.__main += f"set {self.__line_count}: ["
        self.__line_count += 1
        
    def add_green_numb(self, numb):
        self.__main += f"{bcolors.OKGREEN}{numb}{bcolors.ENDC}, "

    def add_red_numb(self, numb):
        self.__main += f"{bcolors.FAIL}{numb}{bcolors.ENDC}, "
        
    def end(self):
        self.__main += "]\n"

    def show(self):
        print(self.__main)


class equal_numbers:

    def __init__(self, number_set, number_sets_file_name):
        self.__input_set = number_set
        self.__number_sets_file = number_sets_file_name
        self.__search = False
    
    def __check_and_enable_search(self, string):
        if "[" in string:
            self.__search = True
    
    def __check_and_disable_search(self, string):
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
        
    def separate(self):
        separated = separated_numbers()
        with open(self.__number_sets_file) as f:
            for line in f.readlines():
                separated.new_line()
                for str_numb in line.split():
                    self.__check_and_enable_search(str_numb)
                    if self.__search:
                        int_str_numb = int(self.__strip_string_number(str_numb))
                        if int_str_numb in self.__input_set:
                            separated.add_green_numb(int_str_numb)
                        else:
                            separated.add_red_numb(int_str_numb)
                    self.__check_and_disable_search(str_numb)
            separated.end()
        return separated


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