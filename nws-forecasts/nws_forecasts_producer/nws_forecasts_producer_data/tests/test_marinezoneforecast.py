"""
Test case for MarineZoneForecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nws_forecasts_producer_data.marinezoneforecast import MarineZoneForecast
from nws_forecasts_producer_data.marineforecastperiod import MarineForecastPeriod


class Test_MarineZoneForecast(unittest.TestCase):
    """
    Test case for MarineZoneForecast
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MarineZoneForecast.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MarineZoneForecast for testing
        """
        instance = MarineZoneForecast(
            zone_id='lfphocvzwrswxgyatiuj',
            zone_name='dfwdmoutjfnrultgogtl',
            product_title='dpsohquqjbkrrwiisxua',
            office_name='txhtcktbxiyeamztnwjn',
            issued_at_text='uouqcpxoulyveshvmxig',
            expires_text='ccnsbebvagsjsrjuawwi',
            wmo_header='didesjimtzwifyindnzj',
            bulletin_awips_id='algzdulonnuxnpwalkfu',
            synopsis='haesuhkltfwhhhrsivae',
            periods=[None, None, None],
            bulletin_text='cyaanqhpsokagcjbkbca'
        )
        return instance

    
    def test_zone_id_property(self):
        """
        Test zone_id property
        """
        test_value = 'lfphocvzwrswxgyatiuj'
        self.instance.zone_id = test_value
        self.assertEqual(self.instance.zone_id, test_value)
    
    def test_zone_name_property(self):
        """
        Test zone_name property
        """
        test_value = 'dfwdmoutjfnrultgogtl'
        self.instance.zone_name = test_value
        self.assertEqual(self.instance.zone_name, test_value)
    
    def test_product_title_property(self):
        """
        Test product_title property
        """
        test_value = 'dpsohquqjbkrrwiisxua'
        self.instance.product_title = test_value
        self.assertEqual(self.instance.product_title, test_value)
    
    def test_office_name_property(self):
        """
        Test office_name property
        """
        test_value = 'txhtcktbxiyeamztnwjn'
        self.instance.office_name = test_value
        self.assertEqual(self.instance.office_name, test_value)
    
    def test_issued_at_text_property(self):
        """
        Test issued_at_text property
        """
        test_value = 'uouqcpxoulyveshvmxig'
        self.instance.issued_at_text = test_value
        self.assertEqual(self.instance.issued_at_text, test_value)
    
    def test_expires_text_property(self):
        """
        Test expires_text property
        """
        test_value = 'ccnsbebvagsjsrjuawwi'
        self.instance.expires_text = test_value
        self.assertEqual(self.instance.expires_text, test_value)
    
    def test_wmo_header_property(self):
        """
        Test wmo_header property
        """
        test_value = 'didesjimtzwifyindnzj'
        self.instance.wmo_header = test_value
        self.assertEqual(self.instance.wmo_header, test_value)
    
    def test_bulletin_awips_id_property(self):
        """
        Test bulletin_awips_id property
        """
        test_value = 'algzdulonnuxnpwalkfu'
        self.instance.bulletin_awips_id = test_value
        self.assertEqual(self.instance.bulletin_awips_id, test_value)
    
    def test_synopsis_property(self):
        """
        Test synopsis property
        """
        test_value = 'haesuhkltfwhhhrsivae'
        self.instance.synopsis = test_value
        self.assertEqual(self.instance.synopsis, test_value)
    
    def test_periods_property(self):
        """
        Test periods property
        """
        test_value = [None, None, None]
        self.instance.periods = test_value
        self.assertEqual(self.instance.periods, test_value)
    
    def test_bulletin_text_property(self):
        """
        Test bulletin_text property
        """
        test_value = 'cyaanqhpsokagcjbkbca'
        self.instance.bulletin_text = test_value
        self.assertEqual(self.instance.bulletin_text, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MarineZoneForecast.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MarineZoneForecast.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

