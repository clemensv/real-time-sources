"""
Test case for PositionReport
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_amqp_producer_data.positionreport import PositionReport
from aisstream_amqp_producer_data.msgtypeenum import MsgTypeenum


class Test_PositionReport(unittest.TestCase):
    """
    Test case for PositionReport
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PositionReport.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PositionReport for testing
        """
        instance = PositionReport(
            mmsi='mzxfdphxhbqckndpjgoj',
            flag='rculvnjaxikjcplfxmhy',
            ship_type='kzrfhghfamionqqiahxv',
            geohash5='wktzwpylmigdscwidnqu',
            msg_type=MsgTypeenum.position_report,
            user_id=int(74),
            latitude=float(59.324212227390696),
            longitude=float(28.09201692273121),
            sog=float(14.711414441801839),
            cog=float(84.53478206323473),
            true_heading=int(4),
            navigational_status=int(74),
            rate_of_turn=int(70),
            position_accuracy=False,
            timestamp=int(74),
            raim=False,
            message_id=int(31)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = 'mzxfdphxhbqckndpjgoj'
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_flag_property(self):
        """
        Test flag property
        """
        test_value = 'rculvnjaxikjcplfxmhy'
        self.instance.flag = test_value
        self.assertEqual(self.instance.flag, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = 'kzrfhghfamionqqiahxv'
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'wktzwpylmigdscwidnqu'
        self.instance.geohash5 = test_value
        self.assertEqual(self.instance.geohash5, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = MsgTypeenum.position_report
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_user_id_property(self):
        """
        Test user_id property
        """
        test_value = int(74)
        self.instance.user_id = test_value
        self.assertEqual(self.instance.user_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(59.324212227390696)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(28.09201692273121)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_sog_property(self):
        """
        Test sog property
        """
        test_value = float(14.711414441801839)
        self.instance.sog = test_value
        self.assertEqual(self.instance.sog, test_value)
    
    def test_cog_property(self):
        """
        Test cog property
        """
        test_value = float(84.53478206323473)
        self.instance.cog = test_value
        self.assertEqual(self.instance.cog, test_value)
    
    def test_true_heading_property(self):
        """
        Test true_heading property
        """
        test_value = int(4)
        self.instance.true_heading = test_value
        self.assertEqual(self.instance.true_heading, test_value)
    
    def test_navigational_status_property(self):
        """
        Test navigational_status property
        """
        test_value = int(74)
        self.instance.navigational_status = test_value
        self.assertEqual(self.instance.navigational_status, test_value)
    
    def test_rate_of_turn_property(self):
        """
        Test rate_of_turn property
        """
        test_value = int(70)
        self.instance.rate_of_turn = test_value
        self.assertEqual(self.instance.rate_of_turn, test_value)
    
    def test_position_accuracy_property(self):
        """
        Test position_accuracy property
        """
        test_value = False
        self.instance.position_accuracy = test_value
        self.assertEqual(self.instance.position_accuracy, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = int(74)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_raim_property(self):
        """
        Test raim property
        """
        test_value = False
        self.instance.raim = test_value
        self.assertEqual(self.instance.raim, test_value)
    
    def test_message_id_property(self):
        """
        Test message_id property
        """
        test_value = int(31)
        self.instance.message_id = test_value
        self.assertEqual(self.instance.message_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PositionReport.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PositionReport.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

