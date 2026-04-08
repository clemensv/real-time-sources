"""
Test case for Site
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from laqn_london_producer_data.uk.kcl.laqn.site import Site


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
            site_code='vutqxghdtzshuxcgtjmb',
            site_name='tnrrolyzshujlgometkp',
            site_type='xrnpdgzpbrtmticjlymd',
            local_authority_code='iubknvdpxelvidybxaxg',
            local_authority_name='pmdwlcnqvvvycuwqpyzk',
            latitude=float(76.89601595701279),
            longitude=float(36.14148198490417),
            date_opened='zekmvoygselfiztjutfj',
            date_closed='bknpdpiwifslxdxtwixq',
            data_owner='wrwylaxmqgwzrogtfuya',
            data_manager='dtlpkeswzyehnnqhzfjx'
        )
        return instance

    
    def test_site_code_property(self):
        """
        Test site_code property
        """
        test_value = 'vutqxghdtzshuxcgtjmb'
        self.instance.site_code = test_value
        self.assertEqual(self.instance.site_code, test_value)
    
    def test_site_name_property(self):
        """
        Test site_name property
        """
        test_value = 'tnrrolyzshujlgometkp'
        self.instance.site_name = test_value
        self.assertEqual(self.instance.site_name, test_value)
    
    def test_site_type_property(self):
        """
        Test site_type property
        """
        test_value = 'xrnpdgzpbrtmticjlymd'
        self.instance.site_type = test_value
        self.assertEqual(self.instance.site_type, test_value)
    
    def test_local_authority_code_property(self):
        """
        Test local_authority_code property
        """
        test_value = 'iubknvdpxelvidybxaxg'
        self.instance.local_authority_code = test_value
        self.assertEqual(self.instance.local_authority_code, test_value)
    
    def test_local_authority_name_property(self):
        """
        Test local_authority_name property
        """
        test_value = 'pmdwlcnqvvvycuwqpyzk'
        self.instance.local_authority_name = test_value
        self.assertEqual(self.instance.local_authority_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(76.89601595701279)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(36.14148198490417)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_date_opened_property(self):
        """
        Test date_opened property
        """
        test_value = 'zekmvoygselfiztjutfj'
        self.instance.date_opened = test_value
        self.assertEqual(self.instance.date_opened, test_value)
    
    def test_date_closed_property(self):
        """
        Test date_closed property
        """
        test_value = 'bknpdpiwifslxdxtwixq'
        self.instance.date_closed = test_value
        self.assertEqual(self.instance.date_closed, test_value)
    
    def test_data_owner_property(self):
        """
        Test data_owner property
        """
        test_value = 'wrwylaxmqgwzrogtfuya'
        self.instance.data_owner = test_value
        self.assertEqual(self.instance.data_owner, test_value)
    
    def test_data_manager_property(self):
        """
        Test data_manager property
        """
        test_value = 'dtlpkeswzyehnnqhzfjx'
        self.instance.data_manager = test_value
        self.assertEqual(self.instance.data_manager, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Site.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
