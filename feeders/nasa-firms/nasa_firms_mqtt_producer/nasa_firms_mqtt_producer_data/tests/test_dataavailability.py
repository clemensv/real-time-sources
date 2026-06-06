"""
Test case for DataAvailability
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nasa_firms_mqtt_producer_data.nasa.firms.dataavailability import DataAvailability
from nasa_firms_mqtt_producer_data.nasa.firms.instrumentenum import InstrumentEnum
import datetime


class Test_DataAvailability(unittest.TestCase):
    """
    Test case for DataAvailability
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DataAvailability.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DataAvailability for testing
        """
        instance = DataAvailability(
            source='irbpgkqoyaopvazztsgc',
            record_id='wlyiyopdrzkaywojiswa',
            data_id='hfljayasydfbqjnqixff',
            min_date=datetime.date.today(),
            max_date=datetime.date.today(),
            instrument=InstrumentEnum.VIIRS,
            satellite='tadjwqwkfqcklqhzdrlq',
            resolution_m=float(11.384044216456335),
            retrieved_at=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_source_property(self):
        """
        Test source property
        """
        test_value = 'irbpgkqoyaopvazztsgc'
        self.instance.source = test_value
        self.assertEqual(self.instance.source, test_value)
    
    def test_record_id_property(self):
        """
        Test record_id property
        """
        test_value = 'wlyiyopdrzkaywojiswa'
        self.instance.record_id = test_value
        self.assertEqual(self.instance.record_id, test_value)
    
    def test_data_id_property(self):
        """
        Test data_id property
        """
        test_value = 'hfljayasydfbqjnqixff'
        self.instance.data_id = test_value
        self.assertEqual(self.instance.data_id, test_value)
    
    def test_min_date_property(self):
        """
        Test min_date property
        """
        test_value = datetime.date.today()
        self.instance.min_date = test_value
        self.assertEqual(self.instance.min_date, test_value)
    
    def test_max_date_property(self):
        """
        Test max_date property
        """
        test_value = datetime.date.today()
        self.instance.max_date = test_value
        self.assertEqual(self.instance.max_date, test_value)
    
    def test_instrument_property(self):
        """
        Test instrument property
        """
        test_value = InstrumentEnum.VIIRS
        self.instance.instrument = test_value
        self.assertEqual(self.instance.instrument, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = 'tadjwqwkfqcklqhzdrlq'
        self.instance.satellite = test_value
        self.assertEqual(self.instance.satellite, test_value)
    
    def test_resolution_m_property(self):
        """
        Test resolution_m property
        """
        test_value = float(11.384044216456335)
        self.instance.resolution_m = test_value
        self.assertEqual(self.instance.resolution_m, test_value)
    
    def test_retrieved_at_property(self):
        """
        Test retrieved_at property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.retrieved_at = test_value
        self.assertEqual(self.instance.retrieved_at, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DataAvailability.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DataAvailability.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

