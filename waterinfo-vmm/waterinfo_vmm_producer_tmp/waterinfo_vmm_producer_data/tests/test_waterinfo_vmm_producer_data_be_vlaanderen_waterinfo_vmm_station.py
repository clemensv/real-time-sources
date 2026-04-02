"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from waterinfo_vmm_producer_data.be.vlaanderen.waterinfo.vmm.station import Station


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
            station_no='yzgftvzupdgvejtsrdkh',
            station_name='jgukifvxwtmkxqmkdkag',
            station_id='fmmgnxbgdlcivlvvmkhz',
            station_latitude=float(20.22064347023369),
            station_longitude=float(73.03147942126121),
            river_name='hqxfkwftuffejiwsouki',
            stationparameter_name='hdprbzceoxgzjxjvaspv',
            ts_id='zmzmdfksrdbcnjaltope',
            ts_unitname='zeppjirrbwuwmctbinea'
        )
        return instance

    
    def test_station_no_property(self):
        """
        Test station_no property
        """
        test_value = 'yzgftvzupdgvejtsrdkh'
        self.instance.station_no = test_value
        self.assertEqual(self.instance.station_no, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'jgukifvxwtmkxqmkdkag'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'fmmgnxbgdlcivlvvmkhz'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_latitude_property(self):
        """
        Test station_latitude property
        """
        test_value = float(20.22064347023369)
        self.instance.station_latitude = test_value
        self.assertEqual(self.instance.station_latitude, test_value)
    
    def test_station_longitude_property(self):
        """
        Test station_longitude property
        """
        test_value = float(73.03147942126121)
        self.instance.station_longitude = test_value
        self.assertEqual(self.instance.station_longitude, test_value)
    
    def test_river_name_property(self):
        """
        Test river_name property
        """
        test_value = 'hqxfkwftuffejiwsouki'
        self.instance.river_name = test_value
        self.assertEqual(self.instance.river_name, test_value)
    
    def test_stationparameter_name_property(self):
        """
        Test stationparameter_name property
        """
        test_value = 'hdprbzceoxgzjxjvaspv'
        self.instance.stationparameter_name = test_value
        self.assertEqual(self.instance.stationparameter_name, test_value)
    
    def test_ts_id_property(self):
        """
        Test ts_id property
        """
        test_value = 'zmzmdfksrdbcnjaltope'
        self.instance.ts_id = test_value
        self.assertEqual(self.instance.ts_id, test_value)
    
    def test_ts_unitname_property(self):
        """
        Test ts_unitname property
        """
        test_value = 'zeppjirrbwuwmctbinea'
        self.instance.ts_unitname = test_value
        self.assertEqual(self.instance.ts_unitname, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
