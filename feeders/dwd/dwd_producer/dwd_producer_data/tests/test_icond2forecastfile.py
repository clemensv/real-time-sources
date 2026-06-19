"""
Test case for IconD2ForecastFile
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.icond2forecastfile import IconD2ForecastFile


class Test_IconD2ForecastFile(unittest.TestCase):
    """
    Test case for IconD2ForecastFile
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_IconD2ForecastFile.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of IconD2ForecastFile for testing
        """
        instance = IconD2ForecastFile(
            file_url='frlvbeoudzutwggbvnox',
            model='rrymsqfdxpxqintacazb',
            file_name='tloddksnagepklunlkvn',
            run='iatddhrrfeaycrahhfvp',
            forecast_hour=int(22),
            parameter='qbsnhrjncqzboyjigkxk',
            level_type='utwbfmtbymxbkhdrsjfi',
            level='wlftbakiqgrklptqmdgm',
            modified='iwetechaxbdmpmnotcce',
            size_bytes=int(55),
            state='nuttucbrrzqpkziswqkc',
            variable='agyzbeeaozkiovcvxkkp',
            file_id='hzequhftjutompxrubno'
        )
        return instance

    
    def test_file_url_property(self):
        """
        Test file_url property
        """
        test_value = 'frlvbeoudzutwggbvnox'
        self.instance.file_url = test_value
        self.assertEqual(self.instance.file_url, test_value)
    
    def test_model_property(self):
        """
        Test model property
        """
        test_value = 'rrymsqfdxpxqintacazb'
        self.instance.model = test_value
        self.assertEqual(self.instance.model, test_value)
    
    def test_file_name_property(self):
        """
        Test file_name property
        """
        test_value = 'tloddksnagepklunlkvn'
        self.instance.file_name = test_value
        self.assertEqual(self.instance.file_name, test_value)
    
    def test_run_property(self):
        """
        Test run property
        """
        test_value = 'iatddhrrfeaycrahhfvp'
        self.instance.run = test_value
        self.assertEqual(self.instance.run, test_value)
    
    def test_forecast_hour_property(self):
        """
        Test forecast_hour property
        """
        test_value = int(22)
        self.instance.forecast_hour = test_value
        self.assertEqual(self.instance.forecast_hour, test_value)
    
    def test_parameter_property(self):
        """
        Test parameter property
        """
        test_value = 'qbsnhrjncqzboyjigkxk'
        self.instance.parameter = test_value
        self.assertEqual(self.instance.parameter, test_value)
    
    def test_level_type_property(self):
        """
        Test level_type property
        """
        test_value = 'utwbfmtbymxbkhdrsjfi'
        self.instance.level_type = test_value
        self.assertEqual(self.instance.level_type, test_value)
    
    def test_level_property(self):
        """
        Test level property
        """
        test_value = 'wlftbakiqgrklptqmdgm'
        self.instance.level = test_value
        self.assertEqual(self.instance.level, test_value)
    
    def test_modified_property(self):
        """
        Test modified property
        """
        test_value = 'iwetechaxbdmpmnotcce'
        self.instance.modified = test_value
        self.assertEqual(self.instance.modified, test_value)
    
    def test_size_bytes_property(self):
        """
        Test size_bytes property
        """
        test_value = int(55)
        self.instance.size_bytes = test_value
        self.assertEqual(self.instance.size_bytes, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'nuttucbrrzqpkziswqkc'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_variable_property(self):
        """
        Test variable property
        """
        test_value = 'agyzbeeaozkiovcvxkkp'
        self.instance.variable = test_value
        self.assertEqual(self.instance.variable, test_value)
    
    def test_file_id_property(self):
        """
        Test file_id property
        """
        test_value = 'hzequhftjutompxrubno'
        self.instance.file_id = test_value
        self.assertEqual(self.instance.file_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = IconD2ForecastFile.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = IconD2ForecastFile.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

