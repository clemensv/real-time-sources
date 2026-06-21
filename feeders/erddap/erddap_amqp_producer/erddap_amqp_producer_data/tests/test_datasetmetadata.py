"""
Test case for DatasetMetadata
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from erddap_amqp_producer_data.datasetmetadata import DatasetMetadata
from erddap_amqp_producer_data.variablemetadata import VariableMetadata


class Test_DatasetMetadata(unittest.TestCase):
    """
    Test case for DatasetMetadata
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DatasetMetadata.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DatasetMetadata for testing
        """
        instance = DatasetMetadata(
            erddap_id='byibrawlxdbtsfguzrma',
            dataset_id='pxxtcvwftdzomtigcbvl',
            base_url='icbmaoikpycfhjfhgoxr',
            title='ycsogfntxfnsncnawcim',
            cdm_data_type='bwjgrjlhotomwuhnuagw',
            min_time='ggwwvuwafyjzbvclhmgh',
            max_time='ifjetyeogmjqpulvwlbn',
            info_url='axqpeimgmdrbsnrrvoue',
            time_variable='dkrcysxkoqenpypxdpfc',
            station_id_variable='fuxmovbovxsvaccclaff',
            global_attributes={'hciowelxmpnzkkuyeuoz': 'xtheiktlziltayjsimtd', 'ocovidychhauiwapnfeo': 'ayfnabtcroerottojick', 'incjuoycwomiunyayxak': 'dkbrddrschxmcooaopvg', 'zwiazxlqixqxhlphopdd': 'rvreftyuqmutnrfcwrdj'},
            variables=[None]
        )
        return instance

    
    def test_erddap_id_property(self):
        """
        Test erddap_id property
        """
        test_value = 'byibrawlxdbtsfguzrma'
        self.instance.erddap_id = test_value
        self.assertEqual(self.instance.erddap_id, test_value)
    
    def test_dataset_id_property(self):
        """
        Test dataset_id property
        """
        test_value = 'pxxtcvwftdzomtigcbvl'
        self.instance.dataset_id = test_value
        self.assertEqual(self.instance.dataset_id, test_value)
    
    def test_base_url_property(self):
        """
        Test base_url property
        """
        test_value = 'icbmaoikpycfhjfhgoxr'
        self.instance.base_url = test_value
        self.assertEqual(self.instance.base_url, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'ycsogfntxfnsncnawcim'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_cdm_data_type_property(self):
        """
        Test cdm_data_type property
        """
        test_value = 'bwjgrjlhotomwuhnuagw'
        self.instance.cdm_data_type = test_value
        self.assertEqual(self.instance.cdm_data_type, test_value)
    
    def test_min_time_property(self):
        """
        Test min_time property
        """
        test_value = 'ggwwvuwafyjzbvclhmgh'
        self.instance.min_time = test_value
        self.assertEqual(self.instance.min_time, test_value)
    
    def test_max_time_property(self):
        """
        Test max_time property
        """
        test_value = 'ifjetyeogmjqpulvwlbn'
        self.instance.max_time = test_value
        self.assertEqual(self.instance.max_time, test_value)
    
    def test_info_url_property(self):
        """
        Test info_url property
        """
        test_value = 'axqpeimgmdrbsnrrvoue'
        self.instance.info_url = test_value
        self.assertEqual(self.instance.info_url, test_value)
    
    def test_time_variable_property(self):
        """
        Test time_variable property
        """
        test_value = 'dkrcysxkoqenpypxdpfc'
        self.instance.time_variable = test_value
        self.assertEqual(self.instance.time_variable, test_value)
    
    def test_station_id_variable_property(self):
        """
        Test station_id_variable property
        """
        test_value = 'fuxmovbovxsvaccclaff'
        self.instance.station_id_variable = test_value
        self.assertEqual(self.instance.station_id_variable, test_value)
    
    def test_global_attributes_property(self):
        """
        Test global_attributes property
        """
        test_value = {'hciowelxmpnzkkuyeuoz': 'xtheiktlziltayjsimtd', 'ocovidychhauiwapnfeo': 'ayfnabtcroerottojick', 'incjuoycwomiunyayxak': 'dkbrddrschxmcooaopvg', 'zwiazxlqixqxhlphopdd': 'rvreftyuqmutnrfcwrdj'}
        self.instance.global_attributes = test_value
        self.assertEqual(self.instance.global_attributes, test_value)
    
    def test_variables_property(self):
        """
        Test variables property
        """
        test_value = [None]
        self.instance.variables = test_value
        self.assertEqual(self.instance.variables, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DatasetMetadata.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DatasetMetadata.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

