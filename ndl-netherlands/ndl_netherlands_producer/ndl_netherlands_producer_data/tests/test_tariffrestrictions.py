"""
Test case for TariffRestrictions
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.tariffrestrictions import TariffRestrictions
from ndl_netherlands_producer_data.reservationenum import ReservationEnum


class Test_TariffRestrictions(unittest.TestCase):
    """
    Test case for TariffRestrictions
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TariffRestrictions.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TariffRestrictions for testing
        """
        instance = TariffRestrictions(
            start_time='sfewbvddvnovjoslhltc',
            end_time='zoeppkkouiefnfrbvmft',
            start_date='hglrrwsiwgewxtmkivll',
            end_date='xjegevgqnmjhybpluvny',
            min_kwh=float(2.579355039075504),
            max_kwh=float(87.01528946857657),
            min_current=float(89.97228073480721),
            max_current=float(87.69555996991845),
            min_power=float(66.47277693721871),
            max_power=float(43.824418254119614),
            min_duration=int(52),
            max_duration=int(5),
            day_of_week={"test": "test"},
            reservation=ReservationEnum.RESERVATION
        )
        return instance

    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'sfewbvddvnovjoslhltc'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'zoeppkkouiefnfrbvmft'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_start_date_property(self):
        """
        Test start_date property
        """
        test_value = 'hglrrwsiwgewxtmkivll'
        self.instance.start_date = test_value
        self.assertEqual(self.instance.start_date, test_value)
    
    def test_end_date_property(self):
        """
        Test end_date property
        """
        test_value = 'xjegevgqnmjhybpluvny'
        self.instance.end_date = test_value
        self.assertEqual(self.instance.end_date, test_value)
    
    def test_min_kwh_property(self):
        """
        Test min_kwh property
        """
        test_value = float(2.579355039075504)
        self.instance.min_kwh = test_value
        self.assertEqual(self.instance.min_kwh, test_value)
    
    def test_max_kwh_property(self):
        """
        Test max_kwh property
        """
        test_value = float(87.01528946857657)
        self.instance.max_kwh = test_value
        self.assertEqual(self.instance.max_kwh, test_value)
    
    def test_min_current_property(self):
        """
        Test min_current property
        """
        test_value = float(89.97228073480721)
        self.instance.min_current = test_value
        self.assertEqual(self.instance.min_current, test_value)
    
    def test_max_current_property(self):
        """
        Test max_current property
        """
        test_value = float(87.69555996991845)
        self.instance.max_current = test_value
        self.assertEqual(self.instance.max_current, test_value)
    
    def test_min_power_property(self):
        """
        Test min_power property
        """
        test_value = float(66.47277693721871)
        self.instance.min_power = test_value
        self.assertEqual(self.instance.min_power, test_value)
    
    def test_max_power_property(self):
        """
        Test max_power property
        """
        test_value = float(43.824418254119614)
        self.instance.max_power = test_value
        self.assertEqual(self.instance.max_power, test_value)
    
    def test_min_duration_property(self):
        """
        Test min_duration property
        """
        test_value = int(52)
        self.instance.min_duration = test_value
        self.assertEqual(self.instance.min_duration, test_value)
    
    def test_max_duration_property(self):
        """
        Test max_duration property
        """
        test_value = int(5)
        self.instance.max_duration = test_value
        self.assertEqual(self.instance.max_duration, test_value)
    
    def test_day_of_week_property(self):
        """
        Test day_of_week property
        """
        test_value = {"test": "test"}
        self.instance.day_of_week = test_value
        self.assertEqual(self.instance.day_of_week, test_value)
    
    def test_reservation_property(self):
        """
        Test reservation property
        """
        test_value = ReservationEnum.RESERVATION
        self.instance.reservation = test_value
        self.assertEqual(self.instance.reservation, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TariffRestrictions.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TariffRestrictions.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

