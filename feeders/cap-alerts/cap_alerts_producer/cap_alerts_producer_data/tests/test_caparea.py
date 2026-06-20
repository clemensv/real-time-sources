"""
Test case for CapArea
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cap_alerts_producer_data.org.oasis.cap.alerts.caparea import CapArea
from cap_alerts_producer_data.org.oasis.cap.alerts.valuepair import ValuePair


class Test_CapArea(unittest.TestCase):
    """
    Test case for CapArea
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CapArea.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CapArea for testing
        """
        instance = CapArea(
            area_desc='nlwuxfzdlfgqvcevarod',
            polygon=['fyyqrvvgingfoqttziqm', 'hmkfngbiarqqxyoqmvxq', 'uoytexmqzhztijpbwqzt'],
            circle=['qqneqbdcfbviqtpjwbbd'],
            geocode=[None],
            altitude=float(81.1638348383263),
            ceiling=float(51.19031213039209)
        )
        return instance

    
    def test_area_desc_property(self):
        """
        Test area_desc property
        """
        test_value = 'nlwuxfzdlfgqvcevarod'
        self.instance.area_desc = test_value
        self.assertEqual(self.instance.area_desc, test_value)
    
    def test_polygon_property(self):
        """
        Test polygon property
        """
        test_value = ['fyyqrvvgingfoqttziqm', 'hmkfngbiarqqxyoqmvxq', 'uoytexmqzhztijpbwqzt']
        self.instance.polygon = test_value
        self.assertEqual(self.instance.polygon, test_value)
    
    def test_circle_property(self):
        """
        Test circle property
        """
        test_value = ['qqneqbdcfbviqtpjwbbd']
        self.instance.circle = test_value
        self.assertEqual(self.instance.circle, test_value)
    
    def test_geocode_property(self):
        """
        Test geocode property
        """
        test_value = [None]
        self.instance.geocode = test_value
        self.assertEqual(self.instance.geocode, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(81.1638348383263)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_ceiling_property(self):
        """
        Test ceiling property
        """
        test_value = float(51.19031213039209)
        self.instance.ceiling = test_value
        self.assertEqual(self.instance.ceiling, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CapArea.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = CapArea.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

