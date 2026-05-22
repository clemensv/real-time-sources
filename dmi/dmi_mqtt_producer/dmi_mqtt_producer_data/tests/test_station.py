"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_mqtt_producer_data.station import Station


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
            station_id='brvbrhnxqyyhopohhzwv',
            wmo_station_id='maaqlqtczgpbxvnboedx',
            wmo_country_code='wjrizyumzilhzslcyvvt',
            name='emcfqrhgxkflsqfdlogd',
            country='drmbzawqsvsjwofbyzqk',
            owner='qqejmkgbdfardlghlcfd',
            region_id='qxnmkyublbfoedxbciki',
            type='xddczuhcnmuklcpdjiqt',
            status='tvfxoftelqtgbnslukwn',
            parameter_id=['urtnlnwpywcouvltiegk', 'bjblzemikhjuxcvqqtnh', 'nfegwkxrdwunxflunbvt', 'ggtwiicrmxohcqxddtqq'],
            latitude=float(64.3749531179157),
            longitude=float(95.7473996082294),
            station_height=float(10.6850923096943),
            barometer_height=float(68.53670018376383),
            anemometer_height=float(28.693094801729412),
            valid_from='rbgvckmsxnkrxtqsqfpa',
            valid_to='juxdgnwmrbtezlrghcry',
            operation_from='cdvhhvuopsixixigoqap',
            operation_to='ihlfluchnmbxmonzmzng',
            created='jxpvqleigityqwhsndjs',
            updated='wjzbbfpstjiznhmrkgbi'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'brvbrhnxqyyhopohhzwv'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_wmo_station_id_property(self):
        """
        Test wmo_station_id property
        """
        test_value = 'maaqlqtczgpbxvnboedx'
        self.instance.wmo_station_id = test_value
        self.assertEqual(self.instance.wmo_station_id, test_value)
    
    def test_wmo_country_code_property(self):
        """
        Test wmo_country_code property
        """
        test_value = 'wjrizyumzilhzslcyvvt'
        self.instance.wmo_country_code = test_value
        self.assertEqual(self.instance.wmo_country_code, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'emcfqrhgxkflsqfdlogd'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'drmbzawqsvsjwofbyzqk'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_owner_property(self):
        """
        Test owner property
        """
        test_value = 'qqejmkgbdfardlghlcfd'
        self.instance.owner = test_value
        self.assertEqual(self.instance.owner, test_value)
    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = 'qxnmkyublbfoedxbciki'
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'xddczuhcnmuklcpdjiqt'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'tvfxoftelqtgbnslukwn'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_parameter_id_property(self):
        """
        Test parameter_id property
        """
        test_value = ['urtnlnwpywcouvltiegk', 'bjblzemikhjuxcvqqtnh', 'nfegwkxrdwunxflunbvt', 'ggtwiicrmxohcqxddtqq']
        self.instance.parameter_id = test_value
        self.assertEqual(self.instance.parameter_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(64.3749531179157)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(95.7473996082294)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_station_height_property(self):
        """
        Test station_height property
        """
        test_value = float(10.6850923096943)
        self.instance.station_height = test_value
        self.assertEqual(self.instance.station_height, test_value)
    
    def test_barometer_height_property(self):
        """
        Test barometer_height property
        """
        test_value = float(68.53670018376383)
        self.instance.barometer_height = test_value
        self.assertEqual(self.instance.barometer_height, test_value)
    
    def test_anemometer_height_property(self):
        """
        Test anemometer_height property
        """
        test_value = float(28.693094801729412)
        self.instance.anemometer_height = test_value
        self.assertEqual(self.instance.anemometer_height, test_value)
    
    def test_valid_from_property(self):
        """
        Test valid_from property
        """
        test_value = 'rbgvckmsxnkrxtqsqfpa'
        self.instance.valid_from = test_value
        self.assertEqual(self.instance.valid_from, test_value)
    
    def test_valid_to_property(self):
        """
        Test valid_to property
        """
        test_value = 'juxdgnwmrbtezlrghcry'
        self.instance.valid_to = test_value
        self.assertEqual(self.instance.valid_to, test_value)
    
    def test_operation_from_property(self):
        """
        Test operation_from property
        """
        test_value = 'cdvhhvuopsixixigoqap'
        self.instance.operation_from = test_value
        self.assertEqual(self.instance.operation_from, test_value)
    
    def test_operation_to_property(self):
        """
        Test operation_to property
        """
        test_value = 'ihlfluchnmbxmonzmzng'
        self.instance.operation_to = test_value
        self.assertEqual(self.instance.operation_to, test_value)
    
    def test_created_property(self):
        """
        Test created property
        """
        test_value = 'jxpvqleigityqwhsndjs'
        self.instance.created = test_value
        self.assertEqual(self.instance.created, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = 'wjzbbfpstjiznhmrkgbi'
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
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

