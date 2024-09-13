import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.alert_types.effect import Effect

class Test_Effect(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        self.instance = Test_Effect.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Effect
        """
        return "NO_SERVICE"
