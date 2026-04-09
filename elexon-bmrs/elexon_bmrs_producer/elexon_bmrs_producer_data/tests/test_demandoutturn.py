"""
Test case for DemandOutturn
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from elexon_bmrs_producer_data.demandoutturn import DemandOutturn
import datetime


class Test_DemandOutturn(unittest.TestCase):
    """
    Test case for DemandOutturn
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DemandOutturn.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DemandOutturn for testing
        """
        instance = DemandOutturn(
            settlement_period=int(18),
            settlement_date='vcttjrcwurfjkmxrmlzq',
            start_time=datetime.datetime.now(datetime.timezone.utc),
            publish_time=datetime.datetime.now(datetime.timezone.utc),
            initial_demand_outturn_mw=float(8.832253389568711),
            initial_transmission_system_demand_outturn_mw=float(47.615121884621445)
        )
        return instance

    
    def test_settlement_period_property(self):
        """
        Test settlement_period property
        """
        test_value = int(18)
        self.instance.settlement_period = test_value
        self.assertEqual(self.instance.settlement_period, test_value)
    
    def test_settlement_date_property(self):
        """
        Test settlement_date property
        """
        test_value = 'vcttjrcwurfjkmxrmlzq'
        self.instance.settlement_date = test_value
        self.assertEqual(self.instance.settlement_date, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_publish_time_property(self):
        """
        Test publish_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.publish_time = test_value
        self.assertEqual(self.instance.publish_time, test_value)
    
    def test_initial_demand_outturn_mw_property(self):
        """
        Test initial_demand_outturn_mw property
        """
        test_value = float(8.832253389568711)
        self.instance.initial_demand_outturn_mw = test_value
        self.assertEqual(self.instance.initial_demand_outturn_mw, test_value)
    
    def test_initial_transmission_system_demand_outturn_mw_property(self):
        """
        Test initial_transmission_system_demand_outturn_mw property
        """
        test_value = float(47.615121884621445)
        self.instance.initial_transmission_system_demand_outturn_mw = test_value
        self.assertEqual(self.instance.initial_transmission_system_demand_outturn_mw, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DemandOutturn.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DemandOutturn.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

