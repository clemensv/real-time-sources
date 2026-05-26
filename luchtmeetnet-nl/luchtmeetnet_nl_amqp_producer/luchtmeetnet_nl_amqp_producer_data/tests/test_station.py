"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from luchtmeetnet_nl_amqp_producer_data.nl.rivm.luchtmeetnet.station import Station


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
            station_number='vvrkrjsdvkbjxsrmgjpn',
            location='dwtzuvnivzgzomchoenf',
            type='lkvslxgtdqjiotfpsbyu',
            organisation='vhejkzzuefjkxctwgwma',
            municipality='mhcqhixwgunvmxyprsxw',
            province='pnzvkubmrhnlcjzolkfl',
            longitude=float(41.45773939943596),
            latitude=float(30.1850191411564),
            year_start='gludukdrfsakvxqijrsc',
            components=['ssivtofgxayqsvyerzwb', 'hxobctzgoekqqyrlxdaw', 'ihxwumsindjhtqwnxcwa', 'vtopukkjmjtdiazztqnc', 'ixuefxzdthwdpaeaqilu']
        )
        return instance

    
    def test_station_number_property(self):
        """
        Test station_number property
        """
        test_value = 'vvrkrjsdvkbjxsrmgjpn'
        self.instance.station_number = test_value
        self.assertEqual(self.instance.station_number, test_value)
    
    def test_location_property(self):
        """
        Test location property
        """
        test_value = 'dwtzuvnivzgzomchoenf'
        self.instance.location = test_value
        self.assertEqual(self.instance.location, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'lkvslxgtdqjiotfpsbyu'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_organisation_property(self):
        """
        Test organisation property
        """
        test_value = 'vhejkzzuefjkxctwgwma'
        self.instance.organisation = test_value
        self.assertEqual(self.instance.organisation, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'mhcqhixwgunvmxyprsxw'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'pnzvkubmrhnlcjzolkfl'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(41.45773939943596)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(30.1850191411564)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_year_start_property(self):
        """
        Test year_start property
        """
        test_value = 'gludukdrfsakvxqijrsc'
        self.instance.year_start = test_value
        self.assertEqual(self.instance.year_start, test_value)
    
    def test_components_property(self):
        """
        Test components property
        """
        test_value = ['ssivtofgxayqsvyerzwb', 'hxobctzgoekqqyrlxdaw', 'ihxwumsindjhtqwnxcwa', 'vtopukkjmjtdiazztqnc', 'ixuefxzdthwdpaeaqilu']
        self.instance.components = test_value
        self.assertEqual(self.instance.components, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

