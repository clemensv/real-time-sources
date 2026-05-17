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
            file_path='uoyfuvvnksqebvhggrka',
            model='hnwomycdjiqmnofvhedu',
            file_name='imtphusacaahvvrxfozd',
            run='xxqsuusrsqcfperpvlra',
            forecast_hour=int(42),
            parameter='uqswsxlrvhixkwnehtup',
            level_type='iehusiokzugnwdplgkan',
            level='mxyozjlwpdzutihaunsv',
            modified='uudtrxopzksbyldrrbvx',
            size_bytes=int(64),
            download_url='rdxnvsjdogplrlgdjqfy'
        )
        return instance

    
    def test_file_path_property(self):
        """
        Test file_path property
        """
        test_value = 'uoyfuvvnksqebvhggrka'
        self.instance.file_path = test_value
        self.assertEqual(self.instance.file_path, test_value)
    
    def test_model_property(self):
        """
        Test model property
        """
        test_value = 'hnwomycdjiqmnofvhedu'
        self.instance.model = test_value
        self.assertEqual(self.instance.model, test_value)
    
    def test_file_name_property(self):
        """
        Test file_name property
        """
        test_value = 'imtphusacaahvvrxfozd'
        self.instance.file_name = test_value
        self.assertEqual(self.instance.file_name, test_value)
    
    def test_run_property(self):
        """
        Test run property
        """
        test_value = 'xxqsuusrsqcfperpvlra'
        self.instance.run = test_value
        self.assertEqual(self.instance.run, test_value)
    
    def test_forecast_hour_property(self):
        """
        Test forecast_hour property
        """
        test_value = int(42)
        self.instance.forecast_hour = test_value
        self.assertEqual(self.instance.forecast_hour, test_value)
    
    def test_parameter_property(self):
        """
        Test parameter property
        """
        test_value = 'uqswsxlrvhixkwnehtup'
        self.instance.parameter = test_value
        self.assertEqual(self.instance.parameter, test_value)
    
    def test_level_type_property(self):
        """
        Test level_type property
        """
        test_value = 'iehusiokzugnwdplgkan'
        self.instance.level_type = test_value
        self.assertEqual(self.instance.level_type, test_value)
    
    def test_level_property(self):
        """
        Test level property
        """
        test_value = 'mxyozjlwpdzutihaunsv'
        self.instance.level = test_value
        self.assertEqual(self.instance.level, test_value)
    
    def test_modified_property(self):
        """
        Test modified property
        """
        test_value = 'uudtrxopzksbyldrrbvx'
        self.instance.modified = test_value
        self.assertEqual(self.instance.modified, test_value)
    
    def test_size_bytes_property(self):
        """
        Test size_bytes property
        """
        test_value = int(64)
        self.instance.size_bytes = test_value
        self.assertEqual(self.instance.size_bytes, test_value)
    
    def test_download_url_property(self):
        """
        Test download_url property
        """
        test_value = 'rdxnvsjdogplrlgdjqfy'
        self.instance.download_url = test_value
        self.assertEqual(self.instance.download_url, test_value)
    
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

