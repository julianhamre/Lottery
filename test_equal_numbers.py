#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 11:16:06 2022

@author: julianhamre
"""

import unittest
import lottery

class test(unittest.TestCase):
    
    def test_detect(self):
        equal = lottery.equal_numbers([4, 5, 6, 7, 16, 20, 22], "test_sets.txt")
        lines, greens = equal.paint()
        bench_greens = [0, 2, 3]
        self.assertEqual(greens, bench_greens)
        equal.show_information()
        
if __name__ == "__main__":
    unittest.main()
        