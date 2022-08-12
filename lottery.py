#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 10:48:08 2022

@author: julianhamre
"""

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

def attempt_append_to_txt(winning_attempt, file):
    f = open(file, "a") 
    f.write(f"{winning_attempt}\n")
    f.close()

def average_attempt(file):
    average = 0
    with open(file) as f:
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


class correct_numbers:

    def __init__(self, drawn_number_set, guessed_number_sets_file):
        self.__drawn_set = drawn_number_set
        self.__guessed_sets = guessed_number_sets_file
        self.__in_number_set = False
    
    def __find_number_set_start(self, string):
        if "[" in string:
            self.__in_number_set = True
    
    def __find_number_set_end(self, string):
        if "]" in string:
            self.__in_number_set = False
    
    def __strip_number_segment(self, str_numb):
        if "[" in str_numb:
            str_numb = str_numb.replace("[", "")
        if "," in str_numb:
            str_numb = str_numb.replace(",", "")
        if "]" in str_numb:
            str_numb = str_numb.replace("]", "")
        return str_numb
        
    def paint(self):
        with open(self.__guessed_sets) as f:
            painted_lines = []
            correct_per_line = []
            for line in f.readlines():
                painted_line = ""
                correct = 0
                for segment in line.split():
                    self.__find_number_set_start(segment)
                    if self.__in_number_set: 
                        numb = int(self.__strip_number_segment(segment))
                        color = string_colors()
                        str_numb = f"{numb}"
                        if numb in self.__drawn_set:
                            segment = segment.replace(str_numb, color.set_green(str_numb))
                            correct += 1
                        else:
                            segment = segment.replace(str_numb, color.set_red(str_numb))
                    painted_line += f"{segment} "
                    self.__find_number_set_end(segment)
                painted_lines.append(painted_line)
                correct_per_line.append(correct)

        return painted_lines, correct_per_line    

    def __show_lines(self, lines):
        for line in lines:
            print(line)

    def __lines_with_most_correct(self, lines, correct):
        mx = max(correct)
        lines_most_correct = []
        for i in range(len(correct)):
            if correct[i] == mx:
                lines_most_correct.append(lines[i])
        return lines_most_correct

    def __singular_or_plural(self, value, singular, plural):
        if value > 1:
            return f"{value} {plural}"
        else:
            return f"{value} {singular}"

    def show_information(self, show_main_part):
        color = string_colors()
        
        introduction = f"checking for {color.set_green('numbers in')} and {color.set_red('numbers not in')} {self.__drawn_set}:"
        print(f"{introduction}")
        
        lines, correct = self.paint()
        if show_main_part:
            print("")
            self.__show_lines(lines)
        
        lines_most_correct = self.__lines_with_most_correct(lines, correct)
        summary = f"\n{self.__singular_or_plural(len(lines_most_correct), 'set', 'sets')} with the most {color.set_green('numbers in')} {self.__drawn_set}\n{max(correct)}/7 correct numbers:\n"
        print(summary)
        self.__show_lines(lines_most_correct)
        
        
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
                self.__file = arg
        

    def execute(self):    
        for i in range(self.__times):
            winning_attempt = play_lottery_until_won()
            loop_count = f"{i+1}/{self.__times},"
            if self.__append:
                attempt_append_to_txt(winning_attempt, self.__file)
                print(loop_count, "appended winning attempt", winning_attempt)
            else:
                print(loop_count, "won in attempt", winning_attempt)


class show_correct_numbers_options:
    
    def __init__(self, arguments):
        arguments = arguments[1:]
        flags = "h"
        full_string_opts = "hide_main_sets"
        opts, args = getopt.getopt(arguments, flags, full_string_opts)
        
        self.__show_main = True
        
        for opt, arg in opts:
            if opt in ["-h"] or opt in ["--hide_main_sets"]:
                self.__show_main = False
    
    def __drawn_numbers(self):
        str_numbs = input("insert drawn number set (format 1 2 3...): ")
        sectioned_numbs = str_numbs.split()
        number_set = []
        for numb in sectioned_numbs:
            number_set.append(int(numb))
        return number_set
    
    def execute(self):
        numbs = self.__drawn_numbers()
        file = input("insert guessed number sets file: ")
        correct = correct_numbers(numbs, file)
        correct.show_information(self.__show_main)


def execute_commands():
    arguments = sys.argv[1:]
    if arguments[0] == "play":
        play_options(arguments).execute()
    elif arguments[0] == "show_correct_numbers":
        show_correct_numbers_options(arguments).execute()
    else:
        single_options(arguments).execute()

if len(sys.argv) > 1:
    execute_commands()