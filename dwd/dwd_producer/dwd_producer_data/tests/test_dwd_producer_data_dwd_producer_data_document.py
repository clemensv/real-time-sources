"""
Test case for Document
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.dwd_producer_data.document import Document


class Test_Document(unittest.TestCase):
    """
    Test case for Document
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Document.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Document for testing
        """
        instance = Document(
            station_id='efljzkyjqwdroiinjicj',
            station_name='zctuymsizbtvproyxlvt',
            latitude=float(95.4768894123881),
            longitude=float(32.19204025742959),
            elevation=float(29.536017294049177),
            state='uwzbseletorcnecbmawg',
            from_date='vvngvgyivcyxgitjgykv',
            to_date='gezevghdyanonbkxqkcu'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'efljzkyjqwdroiinjicj'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'zctuymsizbtvproyxlvt'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(95.4768894123881)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(32.19204025742959)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = float(29.536017294049177)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'uwzbseletorcnecbmawg'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_from_date_property(self):
        """
        Test from_date property
        """
        test_value = 'vvngvgyivcyxgitjgykv'
        self.instance.from_date = test_value
        self.assertEqual(self.instance.from_date, test_value)
    
    def test_to_date_property(self):
        """
        Test to_date property
        """
        test_value = 'gezevghdyanonbkxqkcu'
        self.instance.to_date = test_value
        self.assertEqual(self.instance.to_date, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Document.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
