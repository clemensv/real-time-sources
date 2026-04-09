"""
Test case for RiverStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nepal_bipad_hydrology_producer_data.np.gov.bipad.hydrology.riverstation import RiverStation


class Test_RiverStation(unittest.TestCase):
    """
    Test case for RiverStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RiverStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RiverStation for testing
        """
        instance = RiverStation(
            station_id='ilskqqejzsgtigjjitfl',
            title='jltaornrvrcrtrtocymj',
            basin='usytwexjflfodtmejote',
            latitude=float(94.03546463379378),
            longitude=float(5.258043762856746),
            elevation=int(20),
            danger_level=float(54.330598880595296),
            warning_level=float(10.673735977851017),
            description='hchipxuvzusjophquecz',
            data_source='pkbfyjahdidrsxxtkgcg',
            province=int(76),
            district=int(34),
            municipality=int(76),
            ward=int(19)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ilskqqejzsgtigjjitfl'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'jltaornrvrcrtrtocymj'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'usytwexjflfodtmejote'
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(94.03546463379378)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(5.258043762856746)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = int(20)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_danger_level_property(self):
        """
        Test danger_level property
        """
        test_value = float(54.330598880595296)
        self.instance.danger_level = test_value
        self.assertEqual(self.instance.danger_level, test_value)
    
    def test_warning_level_property(self):
        """
        Test warning_level property
        """
        test_value = float(10.673735977851017)
        self.instance.warning_level = test_value
        self.assertEqual(self.instance.warning_level, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'hchipxuvzusjophquecz'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_data_source_property(self):
        """
        Test data_source property
        """
        test_value = 'pkbfyjahdidrsxxtkgcg'
        self.instance.data_source = test_value
        self.assertEqual(self.instance.data_source, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = int(76)
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_district_property(self):
        """
        Test district property
        """
        test_value = int(34)
        self.instance.district = test_value
        self.assertEqual(self.instance.district, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = int(76)
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_ward_property(self):
        """
        Test ward property
        """
        test_value = int(19)
        self.instance.ward = test_value
        self.assertEqual(self.instance.ward, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RiverStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
