"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from uba_airdata_mqtt_producer_data.de.uba.airdata.station import Station


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
            station_id=int(32),
            station_code='bhldvaplvlkubikeajpk',
            station_name='xwqopvtrtejzggqpbpna',
            station_city='uenyiytrvjcqofsbcldp',
            station_synonym='alchpaznskcngfguaica',
            active_from='fqzoazpjdhwhzmgkwcac',
            active_to='rtfaccyqktgypglopvxa',
            longitude=float(18.026977133613354),
            latitude=float(19.867613334023304),
            network_id=int(57),
            network_code='pxdvtdoffbhtjkhigmgj',
            network_name='qzgfrgozixzouwqzbjqx',
            setting_name='awgnwnfxaaoemjjinlsw',
            setting_short='hfptipflictiswvyetqp',
            type_name='vdecmdnpqcquqvvmdwzx',
            street='nwefhrnrsmhthsbztoez',
            street_nr='xhjgnvjltsunxynnwckc',
            zip_code='hsrkgitjwewskpxkstqg'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(32)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'bhldvaplvlkubikeajpk'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'xwqopvtrtejzggqpbpna'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_station_city_property(self):
        """
        Test station_city property
        """
        test_value = 'uenyiytrvjcqofsbcldp'
        self.instance.station_city = test_value
        self.assertEqual(self.instance.station_city, test_value)
    
    def test_station_synonym_property(self):
        """
        Test station_synonym property
        """
        test_value = 'alchpaznskcngfguaica'
        self.instance.station_synonym = test_value
        self.assertEqual(self.instance.station_synonym, test_value)
    
    def test_active_from_property(self):
        """
        Test active_from property
        """
        test_value = 'fqzoazpjdhwhzmgkwcac'
        self.instance.active_from = test_value
        self.assertEqual(self.instance.active_from, test_value)
    
    def test_active_to_property(self):
        """
        Test active_to property
        """
        test_value = 'rtfaccyqktgypglopvxa'
        self.instance.active_to = test_value
        self.assertEqual(self.instance.active_to, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(18.026977133613354)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(19.867613334023304)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_network_id_property(self):
        """
        Test network_id property
        """
        test_value = int(57)
        self.instance.network_id = test_value
        self.assertEqual(self.instance.network_id, test_value)
    
    def test_network_code_property(self):
        """
        Test network_code property
        """
        test_value = 'pxdvtdoffbhtjkhigmgj'
        self.instance.network_code = test_value
        self.assertEqual(self.instance.network_code, test_value)
    
    def test_network_name_property(self):
        """
        Test network_name property
        """
        test_value = 'qzgfrgozixzouwqzbjqx'
        self.instance.network_name = test_value
        self.assertEqual(self.instance.network_name, test_value)
    
    def test_setting_name_property(self):
        """
        Test setting_name property
        """
        test_value = 'awgnwnfxaaoemjjinlsw'
        self.instance.setting_name = test_value
        self.assertEqual(self.instance.setting_name, test_value)
    
    def test_setting_short_property(self):
        """
        Test setting_short property
        """
        test_value = 'hfptipflictiswvyetqp'
        self.instance.setting_short = test_value
        self.assertEqual(self.instance.setting_short, test_value)
    
    def test_type_name_property(self):
        """
        Test type_name property
        """
        test_value = 'vdecmdnpqcquqvvmdwzx'
        self.instance.type_name = test_value
        self.assertEqual(self.instance.type_name, test_value)
    
    def test_street_property(self):
        """
        Test street property
        """
        test_value = 'nwefhrnrsmhthsbztoez'
        self.instance.street = test_value
        self.assertEqual(self.instance.street, test_value)
    
    def test_street_nr_property(self):
        """
        Test street_nr property
        """
        test_value = 'xhjgnvjltsunxynnwckc'
        self.instance.street_nr = test_value
        self.assertEqual(self.instance.street_nr, test_value)
    
    def test_zip_code_property(self):
        """
        Test zip_code property
        """
        test_value = 'hsrkgitjwewskpxkstqg'
        self.instance.zip_code = test_value
        self.assertEqual(self.instance.zip_code, test_value)
    
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

