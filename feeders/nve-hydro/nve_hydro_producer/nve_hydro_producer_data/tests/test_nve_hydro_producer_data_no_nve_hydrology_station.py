"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nve_hydro_producer_data.no.nve.hydrology.station import Station


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
            station_id='klczpojmmuprzseloycr',
            station_name='lcqcchrktzwxplqvfmiq',
            river_name='wxemcbtfjcbdzfjupedy',
            latitude=float(51.52431633908344),
            longitude=float(44.13819936867775),
            masl=float(86.42736458313094),
            council_name='liitcnrowqfybbezmsaf',
            county_name='okcuwjuxbvsekvlnmjzr',
            drainage_basin_area=float(87.88464823314959)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'klczpojmmuprzseloycr'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'lcqcchrktzwxplqvfmiq'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_river_name_property(self):
        """
        Test river_name property
        """
        test_value = 'wxemcbtfjcbdzfjupedy'
        self.instance.river_name = test_value
        self.assertEqual(self.instance.river_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(51.52431633908344)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(44.13819936867775)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_masl_property(self):
        """
        Test masl property
        """
        test_value = float(86.42736458313094)
        self.instance.masl = test_value
        self.assertEqual(self.instance.masl, test_value)
    
    def test_council_name_property(self):
        """
        Test council_name property
        """
        test_value = 'liitcnrowqfybbezmsaf'
        self.instance.council_name = test_value
        self.assertEqual(self.instance.council_name, test_value)
    
    def test_county_name_property(self):
        """
        Test county_name property
        """
        test_value = 'okcuwjuxbvsekvlnmjzr'
        self.instance.county_name = test_value
        self.assertEqual(self.instance.county_name, test_value)
    
    def test_drainage_basin_area_property(self):
        """
        Test drainage_basin_area property
        """
        test_value = float(87.88464823314959)
        self.instance.drainage_basin_area = test_value
        self.assertEqual(self.instance.drainage_basin_area, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
