"""
Test case for RadarFileProduct
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_mqtt_producer_data.radarfileproduct import RadarFileProduct


class Test_RadarFileProduct(unittest.TestCase):
    """
    Test case for RadarFileProduct
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RadarFileProduct.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RadarFileProduct for testing
        """
        instance = RadarFileProduct(
            file_url='wmlnmkiljetudazfaigx',
            product='klhgcrfiqagtslrjnbdo',
            file_name='jlnzfbcoiypvnpcdhbml',
            modified='xqwbptruvgfhbbvdbgoh',
            size_bytes=int(16),
            file_id='fzrmrfbogpubtlyxnfsp',
            state='wxwwlxyeudlbfxnvqlpv',
            product_type='zfwivtualdrfeylliaqd'
        )
        return instance

    
    def test_file_url_property(self):
        """
        Test file_url property
        """
        test_value = 'wmlnmkiljetudazfaigx'
        self.instance.file_url = test_value
        self.assertEqual(self.instance.file_url, test_value)
    
    def test_product_property(self):
        """
        Test product property
        """
        test_value = 'klhgcrfiqagtslrjnbdo'
        self.instance.product = test_value
        self.assertEqual(self.instance.product, test_value)
    
    def test_file_name_property(self):
        """
        Test file_name property
        """
        test_value = 'jlnzfbcoiypvnpcdhbml'
        self.instance.file_name = test_value
        self.assertEqual(self.instance.file_name, test_value)
    
    def test_modified_property(self):
        """
        Test modified property
        """
        test_value = 'xqwbptruvgfhbbvdbgoh'
        self.instance.modified = test_value
        self.assertEqual(self.instance.modified, test_value)
    
    def test_size_bytes_property(self):
        """
        Test size_bytes property
        """
        test_value = int(16)
        self.instance.size_bytes = test_value
        self.assertEqual(self.instance.size_bytes, test_value)
    
    def test_file_id_property(self):
        """
        Test file_id property
        """
        test_value = 'fzrmrfbogpubtlyxnfsp'
        self.instance.file_id = test_value
        self.assertEqual(self.instance.file_id, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'wxwwlxyeudlbfxnvqlpv'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_product_type_property(self):
        """
        Test product_type property
        """
        test_value = 'zfwivtualdrfeylliaqd'
        self.instance.product_type = test_value
        self.assertEqual(self.instance.product_type, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RadarFileProduct.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RadarFileProduct.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

