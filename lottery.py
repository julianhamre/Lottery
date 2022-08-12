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


class string_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
    def set_green(self, string):
        return f"{self.OKGREEN}{string}{self.ENDC}"
    
    def set_red(self, string):
        return f"{self.FAIL}{string}{self.ENDC}"


class equal_numbers:

    def __init__(self, winning_number_set, number_sets_file_name):
        self.__input_set = winning_number_set
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
        
    def paint(self):
        with open(self.__number_sets_file) as f:
            painted_lines = []
            greens_per_line = []
            for line in f.readlines():
                painted_line = ""
                greens = 0
                for str_numb in line.split():
                    self.__check_and_enable_search(str_numb)
                    if self.__search:
                        int_str_numb = int(self.__strip_string_number(str_numb))
                        color = string_colors()
                        s = f"{int_str_numb}"
                        if int_str_numb in self.__input_set:
                            str_numb = str_numb.replace(s, color.set_green(s))
                            greens += 1
                        else:
                            str_numb = str_numb.replace(s, color.set_red(s))
                    painted_line += f"{str_numb} "
                    self.__check_and_disable_search(str_numb)
                painted_lines.append(painted_line)
                greens_per_line.append(greens)

        return painted_lines, greens_per_line    

    def __show_lines(self, lines):
        for line in lines:
            print(line)

    def __line_indexes_with_most_greens(self, greens):
        mx = max(greens)
        indexes = []
        for i in range(len(greens)):
            if greens[i] == mx:
                indexes.append(i)
        return indexes
    
    def __lines_with_most_greens(self, lines, greens):
        lines_most_greens = []
        for index in self.__line_indexes_with_most_greens(greens):
            lines_most_greens.append(lines[index])
        return lines_most_greens

    def __amount_of_number_sets(self, lines):
        length = len(lines)
        if length > 1:
            return f"{length} sets"
        else:
            return f"{length} set"

    def show_information(self, show_main_part):
        color = string_colors()
        
        introduction = f"checking for {color.set_green('numbers in')} and {color.set_red('numbers not in')} {self.__input_set}:"
        print(f"{introduction}")
        lines, greens = self.paint()
        
        if show_main_part:
            print("")
            self.__show_lines(lines)
        
        lines_most_greens = self.__lines_with_most_greens(lines, greens)
        summary = f"\n{self.__amount_of_number_sets(lines_most_greens)} with the most {color.set_green('numbers in')}, {max(greens)} greens:\n"
        print(summary)
        self.__show_lines(lines_most_greens)
        

        
        
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


class equal_options:
    
    def __init__(self, arguments):
        arguments = arguments[1:]
        flags = "h"
        full_string_opts = "hide_main_sets"
        opts, args = getopt.getopt(arguments, flags, full_string_opts)
        
        self.__show_main = True
        
        for opt, arg in opts:
            if opt in ["-h"] or opt in ["--hide_main_sets"]:
                self.__show_main = False
    
    def __winning_numbers(self):
        str_numbs = input("insert winning number set (format 1 2 3...): ")
        str_numbs = str_numbs.split()
        list_numbs = []
        for numb in str_numbs:
            list_numbs.append(int(numb))
        return list_numbs
    
    def execute(self):
        numbs = self.__winning_numbers()
        file = input("insert number set file: ")
        equal = equal_numbers(numbs, file)
        equal.show_information(self.__show_main)


def execute_commands():
    arguments = sys.argv[1:]
    if arguments[0] == "play":
        play_options(arguments).execute()
    elif arguments[0] == "equal":
        equal_options(arguments).execute()
    else:
        single_options(arguments).execute()

if len(sys.argv) > 1:
    execute_commands()