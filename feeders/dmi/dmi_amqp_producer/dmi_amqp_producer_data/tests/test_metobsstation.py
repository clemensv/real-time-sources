"""
Test case for MetObsStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_amqp_producer_data.metobsstation import MetObsStation
from dmi_amqp_producer_data.countryenum import CountryEnum
import datetime


class Test_MetObsStation(unittest.TestCase):
    """
    Test case for MetObsStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MetObsStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MetObsStation for testing
        """
        instance = MetObsStation(
            station_id='ggnzehogskugzuzeumoi',
            wmo_station_id='iqvsahygzcixbnaefvii',
            wmo_country_code='hgdkhhgdwjvicrvifphh',
            name='pimhwbxswnvpprfzyjgk',
            country=CountryEnum.DNK,
            owner='fbtfopphorwwyfypxwde',
            region_id='xkkvbijuojcugdysyibd',
            type='atpefufpmnrjkbupxqcs',
            status='tbkqmkmvqywzvvlogtgq',
            parameter_id=['stmqtdzaxlzhziiddfoa', 'iisrjuxqlyyataooieog', 'wvkrmwtpbdtnxxbhqnuy'],
            latitude=float(95.30528462520286),
            longitude=float(65.01626688660438),
            station_height=float(70.89189916120154),
            barometer_height=float(66.77047110099082),
            anemometer_height=float(39.47605224488533),
            valid_from=datetime.datetime.now(datetime.timezone.utc),
            valid_to=datetime.datetime.now(datetime.timezone.utc),
            operation_from=datetime.datetime.now(datetime.timezone.utc),
            operation_to=datetime.datetime.now(datetime.timezone.utc),
            created=datetime.datetime.now(datetime.timezone.utc),
            updated=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ggnzehogskugzuzeumoi'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_wmo_station_id_property(self):
        """
        Test wmo_station_id property
        """
        test_value = 'iqvsahygzcixbnaefvii'
        self.instance.wmo_station_id = test_value
        self.assertEqual(self.instance.wmo_station_id, test_value)
    
    def test_wmo_country_code_property(self):
        """
        Test wmo_country_code property
        """
        test_value = 'hgdkhhgdwjvicrvifphh'
        self.instance.wmo_country_code = test_value
        self.assertEqual(self.instance.wmo_country_code, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'pimhwbxswnvpprfzyjgk'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = CountryEnum.DNK
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_owner_property(self):
        """
        Test owner property
        """
        test_value = 'fbtfopphorwwyfypxwde'
        self.instance.owner = test_value
        self.assertEqual(self.instance.owner, test_value)
    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = 'xkkvbijuojcugdysyibd'
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'atpefufpmnrjkbupxqcs'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'tbkqmkmvqywzvvlogtgq'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_parameter_id_property(self):
        """
        Test parameter_id property
        """
        test_value = ['stmqtdzaxlzhziiddfoa', 'iisrjuxqlyyataooieog', 'wvkrmwtpbdtnxxbhqnuy']
        self.instance.parameter_id = test_value
        self.assertEqual(self.instance.parameter_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(95.30528462520286)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(65.01626688660438)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_station_height_property(self):
        """
        Test station_height property
        """
        test_value = float(70.89189916120154)
        self.instance.station_height = test_value
        self.assertEqual(self.instance.station_height, test_value)
    
    def test_barometer_height_property(self):
        """
        Test barometer_height property
        """
        test_value = float(66.77047110099082)
        self.instance.barometer_height = test_value
        self.assertEqual(self.instance.barometer_height, test_value)
    
    def test_anemometer_height_property(self):
        """
        Test anemometer_height property
        """
        test_value = float(39.47605224488533)
        self.instance.anemometer_height = test_value
        self.assertEqual(self.instance.anemometer_height, test_value)
    
    def test_valid_from_property(self):
        """
        Test valid_from property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.valid_from = test_value
        self.assertEqual(self.instance.valid_from, test_value)
    
    def test_valid_to_property(self):
        """
        Test valid_to property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.valid_to = test_value
        self.assertEqual(self.instance.valid_to, test_value)
    
    def test_operation_from_property(self):
        """
        Test operation_from property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.operation_from = test_value
        self.assertEqual(self.instance.operation_from, test_value)
    
    def test_operation_to_property(self):
        """
        Test operation_to property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.operation_to = test_value
        self.assertEqual(self.instance.operation_to, test_value)
    
    def test_created_property(self):
        """
        Test created property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.created = test_value
        self.assertEqual(self.instance.created, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MetObsStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MetObsStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

