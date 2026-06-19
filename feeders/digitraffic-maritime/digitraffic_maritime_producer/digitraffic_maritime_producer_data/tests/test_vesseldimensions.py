"""
Test case for VesselDimensions
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.vesseldimensions import VesselDimensions
import datetime


class Test_VesselDimensions(unittest.TestCase):
    """
    Test case for VesselDimensions
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VesselDimensions.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VesselDimensions for testing
        """
        instance = VesselDimensions(
            tonnage_certificate_issuer='dhsnxzcrremkxwhxdont',
            date_of_issue=datetime.datetime.now(datetime.timezone.utc),
            gross_tonnage=int(83),
            net_tonnage=int(65),
            dead_weight=int(4),
            length=float(9.764321688650412),
            overall_length=float(49.03497877485433),
            height=float(19.200300682068715),
            breadth=float(30.459964097048864),
            draught=float(12.555693745232322),
            max_speed=float(80.06830448026336),
            engine_power='mettyxpxrbmyqkcntxxm'
        )
        return instance

    
    def test_tonnage_certificate_issuer_property(self):
        """
        Test tonnage_certificate_issuer property
        """
        test_value = 'dhsnxzcrremkxwhxdont'
        self.instance.tonnage_certificate_issuer = test_value
        self.assertEqual(self.instance.tonnage_certificate_issuer, test_value)
    
    def test_date_of_issue_property(self):
        """
        Test date_of_issue property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.date_of_issue = test_value
        self.assertEqual(self.instance.date_of_issue, test_value)
    
    def test_gross_tonnage_property(self):
        """
        Test gross_tonnage property
        """
        test_value = int(83)
        self.instance.gross_tonnage = test_value
        self.assertEqual(self.instance.gross_tonnage, test_value)
    
    def test_net_tonnage_property(self):
        """
        Test net_tonnage property
        """
        test_value = int(65)
        self.instance.net_tonnage = test_value
        self.assertEqual(self.instance.net_tonnage, test_value)
    
    def test_dead_weight_property(self):
        """
        Test dead_weight property
        """
        test_value = int(4)
        self.instance.dead_weight = test_value
        self.assertEqual(self.instance.dead_weight, test_value)
    
    def test_length_property(self):
        """
        Test length property
        """
        test_value = float(9.764321688650412)
        self.instance.length = test_value
        self.assertEqual(self.instance.length, test_value)
    
    def test_overall_length_property(self):
        """
        Test overall_length property
        """
        test_value = float(49.03497877485433)
        self.instance.overall_length = test_value
        self.assertEqual(self.instance.overall_length, test_value)
    
    def test_height_property(self):
        """
        Test height property
        """
        test_value = float(19.200300682068715)
        self.instance.height = test_value
        self.assertEqual(self.instance.height, test_value)
    
    def test_breadth_property(self):
        """
        Test breadth property
        """
        test_value = float(30.459964097048864)
        self.instance.breadth = test_value
        self.assertEqual(self.instance.breadth, test_value)
    
    def test_draught_property(self):
        """
        Test draught property
        """
        test_value = float(12.555693745232322)
        self.instance.draught = test_value
        self.assertEqual(self.instance.draught, test_value)
    
    def test_max_speed_property(self):
        """
        Test max_speed property
        """
        test_value = float(80.06830448026336)
        self.instance.max_speed = test_value
        self.assertEqual(self.instance.max_speed, test_value)
    
    def test_engine_power_property(self):
        """
        Test engine_power property
        """
        test_value = 'mettyxpxrbmyqkcntxxm'
        self.instance.engine_power = test_value
        self.assertEqual(self.instance.engine_power, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VesselDimensions.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VesselDimensions.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

