"""
Test case for Site
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from laqn_london_amqp_producer_data.uk.kcl.laqn.site import Site
from laqn_london_amqp_producer_data.uk.kcl.laqn.sitetypeenum import SiteTypeenum


class Test_Site(unittest.TestCase):
    """
    Test case for Site
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Site.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Site for testing
        """
        instance = Site(
            site_code='aahvchlsrwljijnqdeev',
            site_name='yamnnxqzdwcvuvtlwuju',
            site_type=SiteTypeenum.Suburban,
            local_authority_code='hwdlmmeklqavjjmjlxao',
            local_authority_name='faugkgbtsmghuflbkfmf',
            latitude=float(19.210946179901576),
            longitude=float(87.9025443637007),
            date_opened='lwkixfwmiufqkjoigkkw',
            date_closed='cnjozqgtfjfvsbaynuvb',
            data_owner='npdfjmfgfgnemigeesgz',
            data_manager='lbbgklkuiqdpuaaikdci'
        )
        return instance

    
    def test_site_code_property(self):
        """
        Test site_code property
        """
        test_value = 'aahvchlsrwljijnqdeev'
        self.instance.site_code = test_value
        self.assertEqual(self.instance.site_code, test_value)
    
    def test_site_name_property(self):
        """
        Test site_name property
        """
        test_value = 'yamnnxqzdwcvuvtlwuju'
        self.instance.site_name = test_value
        self.assertEqual(self.instance.site_name, test_value)
    
    def test_site_type_property(self):
        """
        Test site_type property
        """
        test_value = SiteTypeenum.Suburban
        self.instance.site_type = test_value
        self.assertEqual(self.instance.site_type, test_value)
    
    def test_local_authority_code_property(self):
        """
        Test local_authority_code property
        """
        test_value = 'hwdlmmeklqavjjmjlxao'
        self.instance.local_authority_code = test_value
        self.assertEqual(self.instance.local_authority_code, test_value)
    
    def test_local_authority_name_property(self):
        """
        Test local_authority_name property
        """
        test_value = 'faugkgbtsmghuflbkfmf'
        self.instance.local_authority_name = test_value
        self.assertEqual(self.instance.local_authority_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(19.210946179901576)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(87.9025443637007)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_date_opened_property(self):
        """
        Test date_opened property
        """
        test_value = 'lwkixfwmiufqkjoigkkw'
        self.instance.date_opened = test_value
        self.assertEqual(self.instance.date_opened, test_value)
    
    def test_date_closed_property(self):
        """
        Test date_closed property
        """
        test_value = 'cnjozqgtfjfvsbaynuvb'
        self.instance.date_closed = test_value
        self.assertEqual(self.instance.date_closed, test_value)
    
    def test_data_owner_property(self):
        """
        Test data_owner property
        """
        test_value = 'npdfjmfgfgnemigeesgz'
        self.instance.data_owner = test_value
        self.assertEqual(self.instance.data_owner, test_value)
    
    def test_data_manager_property(self):
        """
        Test data_manager property
        """
        test_value = 'lbbgklkuiqdpuaaikdci'
        self.instance.data_manager = test_value
        self.assertEqual(self.instance.data_manager, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Site.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Site.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

