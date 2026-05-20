"""
Test case for ControllerPosition
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from vatsim_producer_data.net.vatsim.controllerposition import ControllerPosition


class Test_ControllerPosition(unittest.TestCase):
    """
    Test case for ControllerPosition
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ControllerPosition.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ControllerPosition for testing
        """
        instance = ControllerPosition(
            cid=int(5),
            callsign='hzqaewqdagipdkqmffwh',
            frequency='qtzbqwhdvefzpfdirngs',
            facility=int(89),
            rating=int(71),
            text_atis='dyqxdkpkncqlrpzknaow',
            last_updated='psuwsyhglupvxfgrvaxv'
        )
        return instance

    
    def test_cid_property(self):
        """
        Test cid property
        """
        test_value = int(5)
        self.instance.cid = test_value
        self.assertEqual(self.instance.cid, test_value)
    
    def test_callsign_property(self):
        """
        Test callsign property
        """
        test_value = 'hzqaewqdagipdkqmffwh'
        self.instance.callsign = test_value
        self.assertEqual(self.instance.callsign, test_value)
    
    def test_frequency_property(self):
        """
        Test frequency property
        """
        test_value = 'qtzbqwhdvefzpfdirngs'
        self.instance.frequency = test_value
        self.assertEqual(self.instance.frequency, test_value)
    
    def test_facility_property(self):
        """
        Test facility property
        """
        test_value = int(89)
        self.instance.facility = test_value
        self.assertEqual(self.instance.facility, test_value)
    
    def test_rating_property(self):
        """
        Test rating property
        """
        test_value = int(71)
        self.instance.rating = test_value
        self.assertEqual(self.instance.rating, test_value)
    
    def test_text_atis_property(self):
        """
        Test text_atis property
        """
        test_value = 'dyqxdkpkncqlrpzknaow'
        self.instance.text_atis = test_value
        self.assertEqual(self.instance.text_atis, test_value)
    
    def test_last_updated_property(self):
        """
        Test last_updated property
        """
        test_value = 'psuwsyhglupvxfgrvaxv'
        self.instance.last_updated = test_value
        self.assertEqual(self.instance.last_updated, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ControllerPosition.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
