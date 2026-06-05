"""
Test case for WaitTime
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cbp_border_wait_producer_data.gov.cbp.borderwait.waittime import WaitTime
from cbp_border_wait_producer_data.gov.cbp.borderwait.borderslugenum import BorderSlugenum


class Test_WaitTime(unittest.TestCase):
    """
    Test case for WaitTime
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaitTime.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaitTime for testing
        """
        instance = WaitTime(
            port_number='zpmeshmanwaupoxzcbbc',
            port_name='wnqsrmewtrviiblnsoyd',
            border='ptsqczvxaodlxsclobza',
            crossing_name='tbvkoyhudykycjyuptez',
            port_status='zfkcpkafksukmspllesq',
            date='jilqicxttufxmxqqvege',
            time='umauwyasnkccemapchls',
            passenger_vehicle_standard_delay=int(17),
            passenger_vehicle_standard_lanes_open=int(78),
            passenger_vehicle_standard_operational_status='dliwehvbmbndhqpwthqu',
            passenger_vehicle_nexus_sentri_delay=int(30),
            passenger_vehicle_nexus_sentri_lanes_open=int(31),
            passenger_vehicle_nexus_sentri_operational_status='cynrssizihqgmzzijlrw',
            passenger_vehicle_ready_delay=int(59),
            passenger_vehicle_ready_lanes_open=int(8),
            passenger_vehicle_ready_operational_status='gkgkgbglxbnqofsotgub',
            pedestrian_standard_delay=int(100),
            pedestrian_standard_lanes_open=int(45),
            pedestrian_standard_operational_status='amycrxijsmmzrgssdadd',
            pedestrian_ready_delay=int(46),
            pedestrian_ready_lanes_open=int(81),
            pedestrian_ready_operational_status='zlmuipwaduvajaxrhawg',
            commercial_vehicle_standard_delay=int(39),
            commercial_vehicle_standard_lanes_open=int(42),
            commercial_vehicle_standard_operational_status='jrappwqrqivhsfngsitn',
            commercial_vehicle_fast_delay=int(66),
            commercial_vehicle_fast_lanes_open=int(99),
            commercial_vehicle_fast_operational_status='cdaysxtwycbkittxeswo',
            construction_notice='mfdzrgirmztljfovgikp',
            border_slug=BorderSlugenum.canadian_border
        )
        return instance

    
    def test_port_number_property(self):
        """
        Test port_number property
        """
        test_value = 'zpmeshmanwaupoxzcbbc'
        self.instance.port_number = test_value
        self.assertEqual(self.instance.port_number, test_value)
    
    def test_port_name_property(self):
        """
        Test port_name property
        """
        test_value = 'wnqsrmewtrviiblnsoyd'
        self.instance.port_name = test_value
        self.assertEqual(self.instance.port_name, test_value)
    
    def test_border_property(self):
        """
        Test border property
        """
        test_value = 'ptsqczvxaodlxsclobza'
        self.instance.border = test_value
        self.assertEqual(self.instance.border, test_value)
    
    def test_crossing_name_property(self):
        """
        Test crossing_name property
        """
        test_value = 'tbvkoyhudykycjyuptez'
        self.instance.crossing_name = test_value
        self.assertEqual(self.instance.crossing_name, test_value)
    
    def test_port_status_property(self):
        """
        Test port_status property
        """
        test_value = 'zfkcpkafksukmspllesq'
        self.instance.port_status = test_value
        self.assertEqual(self.instance.port_status, test_value)
    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'jilqicxttufxmxqqvege'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'umauwyasnkccemapchls'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_passenger_vehicle_standard_delay_property(self):
        """
        Test passenger_vehicle_standard_delay property
        """
        test_value = int(17)
        self.instance.passenger_vehicle_standard_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_delay, test_value)
    
    def test_passenger_vehicle_standard_lanes_open_property(self):
        """
        Test passenger_vehicle_standard_lanes_open property
        """
        test_value = int(78)
        self.instance.passenger_vehicle_standard_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_lanes_open, test_value)
    
    def test_passenger_vehicle_standard_operational_status_property(self):
        """
        Test passenger_vehicle_standard_operational_status property
        """
        test_value = 'dliwehvbmbndhqpwthqu'
        self.instance.passenger_vehicle_standard_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_operational_status, test_value)
    
    def test_passenger_vehicle_nexus_sentri_delay_property(self):
        """
        Test passenger_vehicle_nexus_sentri_delay property
        """
        test_value = int(30)
        self.instance.passenger_vehicle_nexus_sentri_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_delay, test_value)
    
    def test_passenger_vehicle_nexus_sentri_lanes_open_property(self):
        """
        Test passenger_vehicle_nexus_sentri_lanes_open property
        """
        test_value = int(31)
        self.instance.passenger_vehicle_nexus_sentri_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_lanes_open, test_value)
    
    def test_passenger_vehicle_nexus_sentri_operational_status_property(self):
        """
        Test passenger_vehicle_nexus_sentri_operational_status property
        """
        test_value = 'cynrssizihqgmzzijlrw'
        self.instance.passenger_vehicle_nexus_sentri_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_operational_status, test_value)
    
    def test_passenger_vehicle_ready_delay_property(self):
        """
        Test passenger_vehicle_ready_delay property
        """
        test_value = int(59)
        self.instance.passenger_vehicle_ready_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_delay, test_value)
    
    def test_passenger_vehicle_ready_lanes_open_property(self):
        """
        Test passenger_vehicle_ready_lanes_open property
        """
        test_value = int(8)
        self.instance.passenger_vehicle_ready_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_lanes_open, test_value)
    
    def test_passenger_vehicle_ready_operational_status_property(self):
        """
        Test passenger_vehicle_ready_operational_status property
        """
        test_value = 'gkgkgbglxbnqofsotgub'
        self.instance.passenger_vehicle_ready_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_operational_status, test_value)
    
    def test_pedestrian_standard_delay_property(self):
        """
        Test pedestrian_standard_delay property
        """
        test_value = int(100)
        self.instance.pedestrian_standard_delay = test_value
        self.assertEqual(self.instance.pedestrian_standard_delay, test_value)
    
    def test_pedestrian_standard_lanes_open_property(self):
        """
        Test pedestrian_standard_lanes_open property
        """
        test_value = int(45)
        self.instance.pedestrian_standard_lanes_open = test_value
        self.assertEqual(self.instance.pedestrian_standard_lanes_open, test_value)
    
    def test_pedestrian_standard_operational_status_property(self):
        """
        Test pedestrian_standard_operational_status property
        """
        test_value = 'amycrxijsmmzrgssdadd'
        self.instance.pedestrian_standard_operational_status = test_value
        self.assertEqual(self.instance.pedestrian_standard_operational_status, test_value)
    
    def test_pedestrian_ready_delay_property(self):
        """
        Test pedestrian_ready_delay property
        """
        test_value = int(46)
        self.instance.pedestrian_ready_delay = test_value
        self.assertEqual(self.instance.pedestrian_ready_delay, test_value)
    
    def test_pedestrian_ready_lanes_open_property(self):
        """
        Test pedestrian_ready_lanes_open property
        """
        test_value = int(81)
        self.instance.pedestrian_ready_lanes_open = test_value
        self.assertEqual(self.instance.pedestrian_ready_lanes_open, test_value)
    
    def test_pedestrian_ready_operational_status_property(self):
        """
        Test pedestrian_ready_operational_status property
        """
        test_value = 'zlmuipwaduvajaxrhawg'
        self.instance.pedestrian_ready_operational_status = test_value
        self.assertEqual(self.instance.pedestrian_ready_operational_status, test_value)
    
    def test_commercial_vehicle_standard_delay_property(self):
        """
        Test commercial_vehicle_standard_delay property
        """
        test_value = int(39)
        self.instance.commercial_vehicle_standard_delay = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_delay, test_value)
    
    def test_commercial_vehicle_standard_lanes_open_property(self):
        """
        Test commercial_vehicle_standard_lanes_open property
        """
        test_value = int(42)
        self.instance.commercial_vehicle_standard_lanes_open = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_lanes_open, test_value)
    
    def test_commercial_vehicle_standard_operational_status_property(self):
        """
        Test commercial_vehicle_standard_operational_status property
        """
        test_value = 'jrappwqrqivhsfngsitn'
        self.instance.commercial_vehicle_standard_operational_status = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_operational_status, test_value)
    
    def test_commercial_vehicle_fast_delay_property(self):
        """
        Test commercial_vehicle_fast_delay property
        """
        test_value = int(66)
        self.instance.commercial_vehicle_fast_delay = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_delay, test_value)
    
    def test_commercial_vehicle_fast_lanes_open_property(self):
        """
        Test commercial_vehicle_fast_lanes_open property
        """
        test_value = int(99)
        self.instance.commercial_vehicle_fast_lanes_open = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_lanes_open, test_value)
    
    def test_commercial_vehicle_fast_operational_status_property(self):
        """
        Test commercial_vehicle_fast_operational_status property
        """
        test_value = 'cdaysxtwycbkittxeswo'
        self.instance.commercial_vehicle_fast_operational_status = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_operational_status, test_value)
    
    def test_construction_notice_property(self):
        """
        Test construction_notice property
        """
        test_value = 'mfdzrgirmztljfovgikp'
        self.instance.construction_notice = test_value
        self.assertEqual(self.instance.construction_notice, test_value)
    
    def test_border_slug_property(self):
        """
        Test border_slug property
        """
        test_value = BorderSlugenum.canadian_border
        self.instance.border_slug = test_value
        self.assertEqual(self.instance.border_slug, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaitTime.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WaitTime.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

