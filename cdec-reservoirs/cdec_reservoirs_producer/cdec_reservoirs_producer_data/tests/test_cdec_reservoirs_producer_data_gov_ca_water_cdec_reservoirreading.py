"""
Test case for ReservoirReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cdec_reservoirs_producer_data.gov.ca.water.cdec.reservoirreading import ReservoirReading


class Test_ReservoirReading(unittest.TestCase):
    """
    Test case for ReservoirReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ReservoirReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ReservoirReading for testing
        """
        instance = ReservoirReading(
            station_id='tgjvqvuigyjaihoqghds',
            sensor_num=int(71),
            sensor_type='pjjfqaaspqcuuqwrnext',
            value=float(47.10210069652453),
            units='gykugvvftafnhrknnipj',
            date='vmaevmlkwkoquwmckkwf',
            dur_code='gpvajnpwrjdoabtorqpo',
            data_flag='hbipyakiiiliddelfrrh'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'tgjvqvuigyjaihoqghds'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_sensor_num_property(self):
        """
        Test sensor_num property
        """
        test_value = int(71)
        self.instance.sensor_num = test_value
        self.assertEqual(self.instance.sensor_num, test_value)
    
    def test_sensor_type_property(self):
        """
        Test sensor_type property
        """
        test_value = 'pjjfqaaspqcuuqwrnext'
        self.instance.sensor_type = test_value
        self.assertEqual(self.instance.sensor_type, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(47.10210069652453)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_units_property(self):
        """
        Test units property
        """
        test_value = 'gykugvvftafnhrknnipj'
        self.instance.units = test_value
        self.assertEqual(self.instance.units, test_value)
    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'vmaevmlkwkoquwmckkwf'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_dur_code_property(self):
        """
        Test dur_code property
        """
        test_value = 'gpvajnpwrjdoabtorqpo'
        self.instance.dur_code = test_value
        self.assertEqual(self.instance.dur_code, test_value)
    
    def test_data_flag_property(self):
        """
        Test data_flag property
        """
        test_value = 'hbipyakiiiliddelfrrh'
        self.instance.data_flag = test_value
        self.assertEqual(self.instance.data_flag, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ReservoirReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
