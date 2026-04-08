"""
Test case for VesselConstruction
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.vesselconstruction import VesselConstruction
import datetime


class Test_VesselConstruction(unittest.TestCase):
    """
    Test case for VesselConstruction
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VesselConstruction.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VesselConstruction for testing
        """
        instance = VesselConstruction(
            vessel_type_code=int(49),
            vessel_type_name='qgjtmksaawxaxhoqualf',
            ice_class_code='odffbjecseffyaofeeqt',
            ice_class_issue_date=datetime.datetime.now(datetime.timezone.utc),
            ice_class_issue_place='crjfamdcldlfjhdnerfo',
            ice_class_end_date=datetime.datetime.now(datetime.timezone.utc),
            double_bottom=False,
            inert_gas_system=False,
            ballast_tank=True
        )
        return instance

    
    def test_vessel_type_code_property(self):
        """
        Test vessel_type_code property
        """
        test_value = int(49)
        self.instance.vessel_type_code = test_value
        self.assertEqual(self.instance.vessel_type_code, test_value)
    
    def test_vessel_type_name_property(self):
        """
        Test vessel_type_name property
        """
        test_value = 'qgjtmksaawxaxhoqualf'
        self.instance.vessel_type_name = test_value
        self.assertEqual(self.instance.vessel_type_name, test_value)
    
    def test_ice_class_code_property(self):
        """
        Test ice_class_code property
        """
        test_value = 'odffbjecseffyaofeeqt'
        self.instance.ice_class_code = test_value
        self.assertEqual(self.instance.ice_class_code, test_value)
    
    def test_ice_class_issue_date_property(self):
        """
        Test ice_class_issue_date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.ice_class_issue_date = test_value
        self.assertEqual(self.instance.ice_class_issue_date, test_value)
    
    def test_ice_class_issue_place_property(self):
        """
        Test ice_class_issue_place property
        """
        test_value = 'crjfamdcldlfjhdnerfo'
        self.instance.ice_class_issue_place = test_value
        self.assertEqual(self.instance.ice_class_issue_place, test_value)
    
    def test_ice_class_end_date_property(self):
        """
        Test ice_class_end_date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.ice_class_end_date = test_value
        self.assertEqual(self.instance.ice_class_end_date, test_value)
    
    def test_double_bottom_property(self):
        """
        Test double_bottom property
        """
        test_value = False
        self.instance.double_bottom = test_value
        self.assertEqual(self.instance.double_bottom, test_value)
    
    def test_inert_gas_system_property(self):
        """
        Test inert_gas_system property
        """
        test_value = False
        self.instance.inert_gas_system = test_value
        self.assertEqual(self.instance.inert_gas_system, test_value)
    
    def test_ballast_tank_property(self):
        """
        Test ballast_tank property
        """
        test_value = True
        self.instance.ballast_tank = test_value
        self.assertEqual(self.instance.ballast_tank, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VesselConstruction.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VesselConstruction.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

