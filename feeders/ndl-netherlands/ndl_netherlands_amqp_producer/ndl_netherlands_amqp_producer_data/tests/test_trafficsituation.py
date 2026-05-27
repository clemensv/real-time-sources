"""
Test case for TrafficSituation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_amqp_producer_data.nl.ndw.traffic.trafficsituation import TrafficSituation


class Test_TrafficSituation(unittest.TestCase):
    """
    Test case for TrafficSituation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TrafficSituation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TrafficSituation for testing
        """
        instance = TrafficSituation(
            situation_id='arqewsenxhlntjlrxipn',
            version_time='hxeawgctrssoneozqqnd',
            severity='zlwzsozytdladpybxtdp',
            record_type='gnjvcxecjwojyllglpwo',
            cause_type='qeivraceqhfbgjdzoqby',
            start_time='alyguqdtdubwggoqsgbi',
            end_time='woidvnewfakcwdzfpoaw',
            information_status='zcgremyaziwbbtfoygfs'
        )
        return instance

    
    def test_situation_id_property(self):
        """
        Test situation_id property
        """
        test_value = 'arqewsenxhlntjlrxipn'
        self.instance.situation_id = test_value
        self.assertEqual(self.instance.situation_id, test_value)
    
    def test_version_time_property(self):
        """
        Test version_time property
        """
        test_value = 'hxeawgctrssoneozqqnd'
        self.instance.version_time = test_value
        self.assertEqual(self.instance.version_time, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'zlwzsozytdladpybxtdp'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_record_type_property(self):
        """
        Test record_type property
        """
        test_value = 'gnjvcxecjwojyllglpwo'
        self.instance.record_type = test_value
        self.assertEqual(self.instance.record_type, test_value)
    
    def test_cause_type_property(self):
        """
        Test cause_type property
        """
        test_value = 'qeivraceqhfbgjdzoqby'
        self.instance.cause_type = test_value
        self.assertEqual(self.instance.cause_type, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'alyguqdtdubwggoqsgbi'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'woidvnewfakcwdzfpoaw'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_information_status_property(self):
        """
        Test information_status property
        """
        test_value = 'zcgremyaziwbbtfoygfs'
        self.instance.information_status = test_value
        self.assertEqual(self.instance.information_status, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TrafficSituation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TrafficSituation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

