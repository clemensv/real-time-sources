"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from luchtmeetnet_nl_producer_data.nl.rivm.luchtmeetnet.station import Station


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
            station_number='fprecemoowaaptjqckvl',
            location='uuzlyymiaelxcbklqpuc',
            type='utykppddtcvyfmyyzwpm',
            organisation='ugyquabdutnotyaoipzx',
            municipality='qwdsiyjhkahdqpxzzivl',
            province='outwugrqcixhglxlnbrm',
            longitude=float(79.65583966942226),
            latitude=float(63.00268949003881),
            year_start='cvnyrlfsgqeypqbowzxc',
            components=['ylrrcardxfdcjyyezecr']
        )
        return instance

    
    def test_station_number_property(self):
        """
        Test station_number property
        """
        test_value = 'fprecemoowaaptjqckvl'
        self.instance.station_number = test_value
        self.assertEqual(self.instance.station_number, test_value)
    
    def test_location_property(self):
        """
        Test location property
        """
        test_value = 'uuzlyymiaelxcbklqpuc'
        self.instance.location = test_value
        self.assertEqual(self.instance.location, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'utykppddtcvyfmyyzwpm'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_organisation_property(self):
        """
        Test organisation property
        """
        test_value = 'ugyquabdutnotyaoipzx'
        self.instance.organisation = test_value
        self.assertEqual(self.instance.organisation, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'qwdsiyjhkahdqpxzzivl'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'outwugrqcixhglxlnbrm'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(79.65583966942226)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(63.00268949003881)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_year_start_property(self):
        """
        Test year_start property
        """
        test_value = 'cvnyrlfsgqeypqbowzxc'
        self.instance.year_start = test_value
        self.assertEqual(self.instance.year_start, test_value)
    
    def test_components_property(self):
        """
        Test components property
        """
        test_value = ['ylrrcardxfdcjyyezecr']
        self.instance.components = test_value
        self.assertEqual(self.instance.components, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
