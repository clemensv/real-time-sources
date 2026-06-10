"""
Test case for TrafficFlowStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_producer_data.us.wa.wsdot.traffic.trafficflowstation import TrafficFlowStation
from wsdot_producer_data.us.wa.wsdot.traffic.regionenum import RegionEnum


class Test_TrafficFlowStation(unittest.TestCase):
    """
    Test case for TrafficFlowStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TrafficFlowStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TrafficFlowStation for testing
        """
        instance = TrafficFlowStation(
            flow_data_id='gthxxempadrfbpjyqnyv',
            station_name='heastctippbbjlhlbkjm',
            region=RegionEnum.Eastern,
            description='jzujezkpailnutdtpnug',
            road_name='lbklzezkmbdwdqfeicjm',
            direction='xbxikozecpyaidkuidgg',
            milepost=float(51.64179953752682),
            latitude=float(17.638055636588334),
            longitude=float(92.42841835120346)
        )
        return instance

    
    def test_flow_data_id_property(self):
        """
        Test flow_data_id property
        """
        test_value = 'gthxxempadrfbpjyqnyv'
        self.instance.flow_data_id = test_value
        self.assertEqual(self.instance.flow_data_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'heastctippbbjlhlbkjm'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = RegionEnum.Eastern
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'jzujezkpailnutdtpnug'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'lbklzezkmbdwdqfeicjm'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_direction_property(self):
        """
        Test direction property
        """
        test_value = 'xbxikozecpyaidkuidgg'
        self.instance.direction = test_value
        self.assertEqual(self.instance.direction, test_value)
    
    def test_milepost_property(self):
        """
        Test milepost property
        """
        test_value = float(51.64179953752682)
        self.instance.milepost = test_value
        self.assertEqual(self.instance.milepost, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(17.638055636588334)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(92.42841835120346)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TrafficFlowStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TrafficFlowStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

