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
        actual = equal.detect()
        bench = [[], [6, 20], [4, 6, 16]]
        self.assertEqual(actual, bench)
        

if __name__ == "__main__":
    unittest.main()
        