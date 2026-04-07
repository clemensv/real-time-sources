"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from imgw_hydro_producer_data.pl.gov.imgw.hydro.station import Station


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
            id_stacji='attmluwhnwoenfrbyfzb',
            stacja='danrxtrvwszjcwkenfcn',
            rzeka='pcmrypuhsfhtraqjinvd',
            wojewodztwo='vrqglaymvtsuenkpwdol',
            longitude=float(48.540404979195884),
            latitude=float(69.21609963355502)
        )
        return instance

    
    def test_id_stacji_property(self):
        """
        Test id_stacji property
        """
        test_value = 'attmluwhnwoenfrbyfzb'
        self.instance.id_stacji = test_value
        self.assertEqual(self.instance.id_stacji, test_value)
    
    def test_stacja_property(self):
        """
        Test stacja property
        """
        test_value = 'danrxtrvwszjcwkenfcn'
        self.instance.stacja = test_value
        self.assertEqual(self.instance.stacja, test_value)
    
    def test_rzeka_property(self):
        """
        Test rzeka property
        """
        test_value = 'pcmrypuhsfhtraqjinvd'
        self.instance.rzeka = test_value
        self.assertEqual(self.instance.rzeka, test_value)
    
    def test_wojewodztwo_property(self):
        """
        Test wojewodztwo property
        """
        test_value = 'vrqglaymvtsuenkpwdol'
        self.instance.wojewodztwo = test_value
        self.assertEqual(self.instance.wojewodztwo, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(48.540404979195884)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(69.21609963355502)
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
