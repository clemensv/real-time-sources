"""
Test case for PositionReportClassB
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_producer_data.positionreportclassb import PositionReportClassB


class Test_PositionReportClassB(unittest.TestCase):
    """
    Test case for PositionReportClassB
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PositionReportClassB.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PositionReportClassB for testing
        """
        instance = PositionReportClassB(
            mmsi=int(23),
            speed_over_ground=float(45.973034398370885),
            position_accuracy=int(49),
            longitude=float(14.217474058137059),
            latitude=float(42.73938271526798),
            course_over_ground=float(9.706309946997859),
            true_heading=int(7),
            timestamp='yanvqkitgqniclmdszpm',
            station_id='jubeenbbksucwlrucyqs',
            msg_type=int(52)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(23)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_speed_over_ground_property(self):
        """
        Test speed_over_ground property
        """
        test_value = float(45.973034398370885)
        self.instance.speed_over_ground = test_value
        self.assertEqual(self.instance.speed_over_ground, test_value)
    
    def test_position_accuracy_property(self):
        """
        Test position_accuracy property
        """
        test_value = int(49)
        self.instance.position_accuracy = test_value
        self.assertEqual(self.instance.position_accuracy, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(14.217474058137059)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(42.73938271526798)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_course_over_ground_property(self):
        """
        Test course_over_ground property
        """
        test_value = float(9.706309946997859)
        self.instance.course_over_ground = test_value
        self.assertEqual(self.instance.course_over_ground, test_value)
    
    def test_true_heading_property(self):
        """
        Test true_heading property
        """
        test_value = int(7)
        self.instance.true_heading = test_value
        self.assertEqual(self.instance.true_heading, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'yanvqkitgqniclmdszpm'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'jubeenbbksucwlrucyqs'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = int(52)
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PositionReportClassB.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PositionReportClassB.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

