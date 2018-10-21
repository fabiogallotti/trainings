"""
Test for the trainings script.

@author: Fabio
"""

import unittest
from trainings import Training

D = 27
M = 6
Y = 1993


class TestTraining(unittest.TestCase):
    def setUp(self):
        self.training = Training(D, M, Y)

    def test_day(self):
        self.assertEqual(self.training.day, D)
    def test_month(self):
        self.assertEqual(self.training.month, M)
    def test_year(self):
        self.assertEqual(self.training.year, Y)
