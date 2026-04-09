"""
Test case for WaitTime
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cbp_border_wait_producer_data.gov.cbp.borderwait.waittime import WaitTime


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
            port_number='cjyjixaldjyineabjhfu',
            port_name='fjuddwaiweqfoewevygr',
            border='lmdsssmdybzshsjeefyh',
            crossing_name='ruzyfczobczqoraywnyh',
            port_status='rdougxwcpbbtlyilgydz',
            date='qehubloreapekfolmjhe',
            time='utczkznbsobzwkjuxfeu',
            passenger_vehicle_standard_delay=int(77),
            passenger_vehicle_standard_lanes_open=int(40),
            passenger_vehicle_standard_operational_status='igervnqkhquxorulrdey',
            passenger_vehicle_nexus_sentri_delay=int(67),
            passenger_vehicle_nexus_sentri_lanes_open=int(23),
            passenger_vehicle_nexus_sentri_operational_status='duvomvthkppkcxtycxwq',
            passenger_vehicle_ready_delay=int(9),
            passenger_vehicle_ready_lanes_open=int(37),
            passenger_vehicle_ready_operational_status='qbrjkfiqtlpmcihxepjx',
            pedestrian_standard_delay=int(64),
            pedestrian_standard_lanes_open=int(95),
            pedestrian_standard_operational_status='mceraddubglqvaamqodc',
            pedestrian_ready_delay=int(45),
            pedestrian_ready_lanes_open=int(92),
            pedestrian_ready_operational_status='lbnbsuxdvlcozwfcgdtg',
            commercial_vehicle_standard_delay=int(46),
            commercial_vehicle_standard_lanes_open=int(46),
            commercial_vehicle_standard_operational_status='qlqpojiwbcrykdzrkyaw',
            commercial_vehicle_fast_delay=int(88),
            commercial_vehicle_fast_lanes_open=int(59),
            commercial_vehicle_fast_operational_status='dntsxctsqzcuvsvulvao',
            construction_notice='tttzczgilnmvdazplpyj'
        )
        return instance

    
    def test_port_number_property(self):
        """
        Test port_number property
        """
        test_value = 'cjyjixaldjyineabjhfu'
        self.instance.port_number = test_value
        self.assertEqual(self.instance.port_number, test_value)
    
    def test_port_name_property(self):
        """
        Test port_name property
        """
        test_value = 'fjuddwaiweqfoewevygr'
        self.instance.port_name = test_value
        self.assertEqual(self.instance.port_name, test_value)
    
    def test_border_property(self):
        """
        Test border property
        """
        test_value = 'lmdsssmdybzshsjeefyh'
        self.instance.border = test_value
        self.assertEqual(self.instance.border, test_value)
    
    def test_crossing_name_property(self):
        """
        Test crossing_name property
        """
        test_value = 'ruzyfczobczqoraywnyh'
        self.instance.crossing_name = test_value
        self.assertEqual(self.instance.crossing_name, test_value)
    
    def test_port_status_property(self):
        """
        Test port_status property
        """
        test_value = 'rdougxwcpbbtlyilgydz'
        self.instance.port_status = test_value
        self.assertEqual(self.instance.port_status, test_value)
    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'qehubloreapekfolmjhe'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'utczkznbsobzwkjuxfeu'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_passenger_vehicle_standard_delay_property(self):
        """
        Test passenger_vehicle_standard_delay property
        """
        test_value = int(77)
        self.instance.passenger_vehicle_standard_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_delay, test_value)
    
    def test_passenger_vehicle_standard_lanes_open_property(self):
        """
        Test passenger_vehicle_standard_lanes_open property
        """
        test_value = int(40)
        self.instance.passenger_vehicle_standard_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_lanes_open, test_value)
    
    def test_passenger_vehicle_standard_operational_status_property(self):
        """
        Test passenger_vehicle_standard_operational_status property
        """
        test_value = 'igervnqkhquxorulrdey'
        self.instance.passenger_vehicle_standard_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_operational_status, test_value)
    
    def test_passenger_vehicle_nexus_sentri_delay_property(self):
        """
        Test passenger_vehicle_nexus_sentri_delay property
        """
        test_value = int(67)
        self.instance.passenger_vehicle_nexus_sentri_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_delay, test_value)
    
    def test_passenger_vehicle_nexus_sentri_lanes_open_property(self):
        """
        Test passenger_vehicle_nexus_sentri_lanes_open property
        """
        test_value = int(23)
        self.instance.passenger_vehicle_nexus_sentri_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_lanes_open, test_value)
    
    def test_passenger_vehicle_nexus_sentri_operational_status_property(self):
        """
        Test passenger_vehicle_nexus_sentri_operational_status property
        """
        test_value = 'duvomvthkppkcxtycxwq'
        self.instance.passenger_vehicle_nexus_sentri_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_operational_status, test_value)
    
    def test_passenger_vehicle_ready_delay_property(self):
        """
        Test passenger_vehicle_ready_delay property
        """
        test_value = int(9)
        self.instance.passenger_vehicle_ready_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_delay, test_value)
    
    def test_passenger_vehicle_ready_lanes_open_property(self):
        """
        Test passenger_vehicle_ready_lanes_open property
        """
        test_value = int(37)
        self.instance.passenger_vehicle_ready_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_lanes_open, test_value)
    
    def test_passenger_vehicle_ready_operational_status_property(self):
        """
        Test passenger_vehicle_ready_operational_status property
        """
        test_value = 'qbrjkfiqtlpmcihxepjx'
        self.instance.passenger_vehicle_ready_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_operational_status, test_value)
    
    def test_pedestrian_standard_delay_property(self):
        """
        Test pedestrian_standard_delay property
        """
        test_value = int(64)
        self.instance.pedestrian_standard_delay = test_value
        self.assertEqual(self.instance.pedestrian_standard_delay, test_value)
    
    def test_pedestrian_standard_lanes_open_property(self):
        """
        Test pedestrian_standard_lanes_open property
        """
        test_value = int(95)
        self.instance.pedestrian_standard_lanes_open = test_value
        self.assertEqual(self.instance.pedestrian_standard_lanes_open, test_value)
    
    def test_pedestrian_standard_operational_status_property(self):
        """
        Test pedestrian_standard_operational_status property
        """
        test_value = 'mceraddubglqvaamqodc'
        self.instance.pedestrian_standard_operational_status = test_value
        self.assertEqual(self.instance.pedestrian_standard_operational_status, test_value)
    
    def test_pedestrian_ready_delay_property(self):
        """
        Test pedestrian_ready_delay property
        """
        test_value = int(45)
        self.instance.pedestrian_ready_delay = test_value
        self.assertEqual(self.instance.pedestrian_ready_delay, test_value)
    
    def test_pedestrian_ready_lanes_open_property(self):
        """
        Test pedestrian_ready_lanes_open property
        """
        test_value = int(92)
        self.instance.pedestrian_ready_lanes_open = test_value
        self.assertEqual(self.instance.pedestrian_ready_lanes_open, test_value)
    
    def test_pedestrian_ready_operational_status_property(self):
        """
        Test pedestrian_ready_operational_status property
        """
        test_value = 'lbnbsuxdvlcozwfcgdtg'
        self.instance.pedestrian_ready_operational_status = test_value
        self.assertEqual(self.instance.pedestrian_ready_operational_status, test_value)
    
    def test_commercial_vehicle_standard_delay_property(self):
        """
        Test commercial_vehicle_standard_delay property
        """
        test_value = int(46)
        self.instance.commercial_vehicle_standard_delay = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_delay, test_value)
    
    def test_commercial_vehicle_standard_lanes_open_property(self):
        """
        Test commercial_vehicle_standard_lanes_open property
        """
        test_value = int(46)
        self.instance.commercial_vehicle_standard_lanes_open = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_lanes_open, test_value)
    
    def test_commercial_vehicle_standard_operational_status_property(self):
        """
        Test commercial_vehicle_standard_operational_status property
        """
        test_value = 'qlqpojiwbcrykdzrkyaw'
        self.instance.commercial_vehicle_standard_operational_status = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_operational_status, test_value)
    
    def test_commercial_vehicle_fast_delay_property(self):
        """
        Test commercial_vehicle_fast_delay property
        """
        test_value = int(88)
        self.instance.commercial_vehicle_fast_delay = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_delay, test_value)
    
    def test_commercial_vehicle_fast_lanes_open_property(self):
        """
        Test commercial_vehicle_fast_lanes_open property
        """
        test_value = int(59)
        self.instance.commercial_vehicle_fast_lanes_open = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_lanes_open, test_value)
    
    def test_commercial_vehicle_fast_operational_status_property(self):
        """
        Test commercial_vehicle_fast_operational_status property
        """
        test_value = 'dntsxctsqzcuvsvulvao'
        self.instance.commercial_vehicle_fast_operational_status = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_operational_status, test_value)
    
    def test_construction_notice_property(self):
        """
        Test construction_notice property
        """
        test_value = 'tttzczgilnmvdazplpyj'
        self.instance.construction_notice = test_value
        self.assertEqual(self.instance.construction_notice, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaitTime.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
