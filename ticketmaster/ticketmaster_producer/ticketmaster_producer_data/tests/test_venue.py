"""
Test case for Venue
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ticketmaster_producer_data.ticketmaster.reference.venue import Venue


class Test_Venue(unittest.TestCase):
    """
    Test case for Venue
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Venue.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Venue for testing
        """
        instance = Venue(
            entity_id='bsxyhwufswkspdlzfacn',
            name='wpsacdlcxievsnpopody',
            url='qcypbdhymvppctwwzqeg',
            locale='lormxuuheqeyhkwybsey',
            timezone='mauymozfgmdfjccaezxv',
            city='jsoapdkxvxreznaihjig',
            state_code='zybzvccjmigirgkgfbwe',
            country_code='amhfuzgxsczdairpuvrx',
            address='nmpjyuexwudglgabjbnd',
            postal_code='skhzzwxctobxrhlcpqbx',
            latitude=float(36.36569137654596),
            longitude=float(4.676989166833234)
        )
        return instance


    def test_entity_id_property(self):
        """
        Test entity_id property
        """
        test_value = 'bsxyhwufswkspdlzfacn'
        self.instance.entity_id = test_value
        self.assertEqual(self.instance.entity_id, test_value)

    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'wpsacdlcxievsnpopody'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)

    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'qcypbdhymvppctwwzqeg'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)

    def test_locale_property(self):
        """
        Test locale property
        """
        test_value = 'lormxuuheqeyhkwybsey'
        self.instance.locale = test_value
        self.assertEqual(self.instance.locale, test_value)

    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'mauymozfgmdfjccaezxv'
        self.instance.timezone = test_value
        self.assertEqual(self.instance.timezone, test_value)

    def test_city_property(self):
        """
        Test city property
        """
        test_value = 'jsoapdkxvxreznaihjig'
        self.instance.city = test_value
        self.assertEqual(self.instance.city, test_value)

    def test_state_code_property(self):
        """
        Test state_code property
        """
        test_value = 'zybzvccjmigirgkgfbwe'
        self.instance.state_code = test_value
        self.assertEqual(self.instance.state_code, test_value)

    def test_country_code_property(self):
        """
        Test country_code property
        """
        test_value = 'amhfuzgxsczdairpuvrx'
        self.instance.country_code = test_value
        self.assertEqual(self.instance.country_code, test_value)

    def test_address_property(self):
        """
        Test address property
        """
        test_value = 'nmpjyuexwudglgabjbnd'
        self.instance.address = test_value
        self.assertEqual(self.instance.address, test_value)

    def test_postal_code_property(self):
        """
        Test postal_code property
        """
        test_value = 'skhzzwxctobxrhlcpqbx'
        self.instance.postal_code = test_value
        self.assertEqual(self.instance.postal_code, test_value)

    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(36.36569137654596)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)

    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(4.676989166833234)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)

    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Venue.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Venue.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Venue.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

