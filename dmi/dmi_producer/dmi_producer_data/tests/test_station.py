"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_producer_data.station import Station


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
            station_id='hkyzflvqvvmmgvvnqrll',
            wmo_station_id='uytwpdivgvuwzndkfxnh',
            wmo_country_code='elihyqzfysiwjuexyzek',
            name='geuuziaeyudyfwjdfjdb',
            country='vlgpvmjshfqnhanxpzoj',
            owner='zswjjqoixjsbdkntwdhn',
            region_id='gbpfljvoqwhumandrvqu',
            type='jqkdnnmvjjjxnbzcozjf',
            status='wktiktvwgjsulsftlfey',
            parameter_id=['zohsvnhkujjtwwjzmjfc', 'akcduqmwodwupblrtjej', 'ufzaawauyhsvkkdtmizh', 'nworsybmpuamjwvaaecy', 'vkxuubainwkurhyuiefv'],
            latitude=float(99.50102052634274),
            longitude=float(25.28144739060635),
            station_height=float(24.110025366952726),
            barometer_height=float(89.6709240355987),
            anemometer_height=float(74.49331251233386),
            valid_from='wmozzoysstkxlaedtkcj',
            valid_to='zphbnwlwwavkkkiggjzn',
            operation_from='vmcbitxmfszenwcluwyi',
            operation_to='qitjpfeugtcbiuetaupe',
            created='jwgkgauedjhbdzuyctne',
            updated='iwqdmkhanhpkeavmzzcv'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'hkyzflvqvvmmgvvnqrll'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_wmo_station_id_property(self):
        """
        Test wmo_station_id property
        """
        test_value = 'uytwpdivgvuwzndkfxnh'
        self.instance.wmo_station_id = test_value
        self.assertEqual(self.instance.wmo_station_id, test_value)
    
    def test_wmo_country_code_property(self):
        """
        Test wmo_country_code property
        """
        test_value = 'elihyqzfysiwjuexyzek'
        self.instance.wmo_country_code = test_value
        self.assertEqual(self.instance.wmo_country_code, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'geuuziaeyudyfwjdfjdb'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'vlgpvmjshfqnhanxpzoj'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_owner_property(self):
        """
        Test owner property
        """
        test_value = 'zswjjqoixjsbdkntwdhn'
        self.instance.owner = test_value
        self.assertEqual(self.instance.owner, test_value)
    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = 'gbpfljvoqwhumandrvqu'
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'jqkdnnmvjjjxnbzcozjf'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'wktiktvwgjsulsftlfey'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_parameter_id_property(self):
        """
        Test parameter_id property
        """
        test_value = ['zohsvnhkujjtwwjzmjfc', 'akcduqmwodwupblrtjej', 'ufzaawauyhsvkkdtmizh', 'nworsybmpuamjwvaaecy', 'vkxuubainwkurhyuiefv']
        self.instance.parameter_id = test_value
        self.assertEqual(self.instance.parameter_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(99.50102052634274)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(25.28144739060635)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_station_height_property(self):
        """
        Test station_height property
        """
        test_value = float(24.110025366952726)
        self.instance.station_height = test_value
        self.assertEqual(self.instance.station_height, test_value)
    
    def test_barometer_height_property(self):
        """
        Test barometer_height property
        """
        test_value = float(89.6709240355987)
        self.instance.barometer_height = test_value
        self.assertEqual(self.instance.barometer_height, test_value)
    
    def test_anemometer_height_property(self):
        """
        Test anemometer_height property
        """
        test_value = float(74.49331251233386)
        self.instance.anemometer_height = test_value
        self.assertEqual(self.instance.anemometer_height, test_value)
    
    def test_valid_from_property(self):
        """
        Test valid_from property
        """
        test_value = 'wmozzoysstkxlaedtkcj'
        self.instance.valid_from = test_value
        self.assertEqual(self.instance.valid_from, test_value)
    
    def test_valid_to_property(self):
        """
        Test valid_to property
        """
        test_value = 'zphbnwlwwavkkkiggjzn'
        self.instance.valid_to = test_value
        self.assertEqual(self.instance.valid_to, test_value)
    
    def test_operation_from_property(self):
        """
        Test operation_from property
        """
        test_value = 'vmcbitxmfszenwcluwyi'
        self.instance.operation_from = test_value
        self.assertEqual(self.instance.operation_from, test_value)
    
    def test_operation_to_property(self):
        """
        Test operation_to property
        """
        test_value = 'qitjpfeugtcbiuetaupe'
        self.instance.operation_to = test_value
        self.assertEqual(self.instance.operation_to, test_value)
    
    def test_created_property(self):
        """
        Test created property
        """
        test_value = 'jwgkgauedjhbdzuyctne'
        self.instance.created = test_value
        self.assertEqual(self.instance.created, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = 'iwqdmkhanhpkeavmzzcv'
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

