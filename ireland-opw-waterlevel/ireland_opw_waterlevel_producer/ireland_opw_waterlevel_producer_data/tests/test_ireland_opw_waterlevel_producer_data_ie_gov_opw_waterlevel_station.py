"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ireland_opw_waterlevel_producer_data.ie.gov.opw.waterlevel.station import Station


class Test_Station(unittest.TestCase):
    """
    Test case for Station
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station for testing
        """
        instance = Station(
            station_ref='ficzutagvpjilmeasvhm',
            station_name='cqfihaduorkgtelieyea',
            region_id=int(97),
            longitude=float(0.962404021308183),
            latitude=float(68.77718722195584)
        )
        return instance

    
    def test_station_ref_property(self):
        """
        Test station_ref property
        """
        test_value = 'ficzutagvpjilmeasvhm'
        self.instance.station_ref = test_value
        self.assertEqual(self.instance.station_ref, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'cqfihaduorkgtelieyea'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = int(97)
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(0.962404021308183)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(68.77718722195584)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
