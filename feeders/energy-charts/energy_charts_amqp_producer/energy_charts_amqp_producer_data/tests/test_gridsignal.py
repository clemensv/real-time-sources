"""
Test case for GridSignal
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from energy_charts_amqp_producer_data.gridsignal import GridSignal
import datetime


class Test_GridSignal(unittest.TestCase):
    """
    Test case for GridSignal
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_GridSignal.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of GridSignal for testing
        """
        instance = GridSignal(
            country='sucdkbdbudmisdokdacg',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            unix_seconds=int(23),
            signal=int(8),
            renewable_share_pct=float(60.79902307509033),
            substitute=True
        )
        return instance

    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'sucdkbdbudmisdokdacg'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_unix_seconds_property(self):
        """
        Test unix_seconds property
        """
        test_value = int(23)
        self.instance.unix_seconds = test_value
        self.assertEqual(self.instance.unix_seconds, test_value)
    
    def test_signal_property(self):
        """
        Test signal property
        """
        test_value = int(8)
        self.instance.signal = test_value
        self.assertEqual(self.instance.signal, test_value)
    
    def test_renewable_share_pct_property(self):
        """
        Test renewable_share_pct property
        """
        test_value = float(60.79902307509033)
        self.instance.renewable_share_pct = test_value
        self.assertEqual(self.instance.renewable_share_pct, test_value)
    
    def test_substitute_property(self):
        """
        Test substitute property
        """
        test_value = True
        self.instance.substitute = test_value
        self.assertEqual(self.instance.substitute, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = GridSignal.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = GridSignal.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

