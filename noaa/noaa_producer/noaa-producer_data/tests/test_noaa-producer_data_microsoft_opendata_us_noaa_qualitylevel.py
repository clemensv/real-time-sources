import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa-producer_data.microsoft.opendata.us.noaa.qualitylevel import QualityLevel

class Test_QualityLevel(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        self.instance = Test_QualityLevel.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of QualityLevel
        """
        return "Preliminary"
