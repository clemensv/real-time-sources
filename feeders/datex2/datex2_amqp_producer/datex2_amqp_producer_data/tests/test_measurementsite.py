"""
Test case for MeasurementSite
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from datex2_amqp_producer_data.org.datex2.measured.measurementsite import MeasurementSite


class Test_MeasurementSite(unittest.TestCase):
    """
    Test case for MeasurementSite
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MeasurementSite.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MeasurementSite for testing
        """
        instance = MeasurementSite(
            supplier_id='uqojcgwuazxuyoqihtxq',
            measurement_site_id='hballkzxwefzdqdtmuzw',
            feed_url='wkxilbymblztuszhdyrl',
            country_code='mnbaynqpupiageyuigen',
            operator_id='qupqgtqsrtakbrasmmvn',
            name='zipfbcuqxzdczcakssop',
            measurement_site_type='gpcaspbkcgvhdzwtgoik',
            period_seconds=int(69),
            latitude=float(74.30130780784818),
            longitude=float(87.58011633373486),
            road_number='kqozozgudafrufttttdj',
            carriageway='dgvaxxjhinykpkuimlxs',
            lane='bfzzqhuvxuujkyyrmgsn',
            specific_measurements='mhfmbweddkqlckuujjqi'
        )
        return instance

    
    def test_supplier_id_property(self):
        """
        Test supplier_id property
        """
        test_value = 'uqojcgwuazxuyoqihtxq'
        self.instance.supplier_id = test_value
        self.assertEqual(self.instance.supplier_id, test_value)
    
    def test_measurement_site_id_property(self):
        """
        Test measurement_site_id property
        """
        test_value = 'hballkzxwefzdqdtmuzw'
        self.instance.measurement_site_id = test_value
        self.assertEqual(self.instance.measurement_site_id, test_value)
    
    def test_feed_url_property(self):
        """
        Test feed_url property
        """
        test_value = 'wkxilbymblztuszhdyrl'
        self.instance.feed_url = test_value
        self.assertEqual(self.instance.feed_url, test_value)
    
    def test_country_code_property(self):
        """
        Test country_code property
        """
        test_value = 'mnbaynqpupiageyuigen'
        self.instance.country_code = test_value
        self.assertEqual(self.instance.country_code, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = 'qupqgtqsrtakbrasmmvn'
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'zipfbcuqxzdczcakssop'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_measurement_site_type_property(self):
        """
        Test measurement_site_type property
        """
        test_value = 'gpcaspbkcgvhdzwtgoik'
        self.instance.measurement_site_type = test_value
        self.assertEqual(self.instance.measurement_site_type, test_value)
    
    def test_period_seconds_property(self):
        """
        Test period_seconds property
        """
        test_value = int(69)
        self.instance.period_seconds = test_value
        self.assertEqual(self.instance.period_seconds, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(74.30130780784818)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(87.58011633373486)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_road_number_property(self):
        """
        Test road_number property
        """
        test_value = 'kqozozgudafrufttttdj'
        self.instance.road_number = test_value
        self.assertEqual(self.instance.road_number, test_value)
    
    def test_carriageway_property(self):
        """
        Test carriageway property
        """
        test_value = 'dgvaxxjhinykpkuimlxs'
        self.instance.carriageway = test_value
        self.assertEqual(self.instance.carriageway, test_value)
    
    def test_lane_property(self):
        """
        Test lane property
        """
        test_value = 'bfzzqhuvxuujkyyrmgsn'
        self.instance.lane = test_value
        self.assertEqual(self.instance.lane, test_value)
    
    def test_specific_measurements_property(self):
        """
        Test specific_measurements property
        """
        test_value = 'mhfmbweddkqlckuujjqi'
        self.instance.specific_measurements = test_value
        self.assertEqual(self.instance.specific_measurements, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MeasurementSite.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MeasurementSite.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

