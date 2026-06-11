"""
Test case for HighwayCamera
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_amqp_producer_data.us.wa.wsdot.cameras.highwaycamera import HighwayCamera


class Test_HighwayCamera(unittest.TestCase):
    """
    Test case for HighwayCamera
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_HighwayCamera.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of HighwayCamera for testing
        """
        instance = HighwayCamera(
            camera_id='jxtvayapuuiztpyeesoc',
            title='pcgpzpdvxxmdxknhjwrl',
            description='zydenmfaqaahypqnzhge',
            camera_owner='ubgofsjcnlcxfcwfcwgu',
            owner_url='stlscgpiodizsesmjzek',
            image_url='qedzllmsymugaagbcyoy',
            image_width=int(0),
            image_height=int(92),
            is_active=True,
            region='ohcwwsbldlrzebmqjrxj',
            sort_order=int(31),
            display_latitude=float(92.2385517242461),
            display_longitude=float(85.08958042992533),
            location_description='labxvqinmjqyxjzidtqi',
            location_direction='nmzwhfvuxouxurpsanyw',
            location_road_name='nngqetzlzftiikayqlch',
            location_milepost=float(66.68529093940218),
            location_latitude=float(46.869842349717686),
            location_longitude=float(64.08420685615083)
        )
        return instance

    
    def test_camera_id_property(self):
        """
        Test camera_id property
        """
        test_value = 'jxtvayapuuiztpyeesoc'
        self.instance.camera_id = test_value
        self.assertEqual(self.instance.camera_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'pcgpzpdvxxmdxknhjwrl'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'zydenmfaqaahypqnzhge'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_camera_owner_property(self):
        """
        Test camera_owner property
        """
        test_value = 'ubgofsjcnlcxfcwfcwgu'
        self.instance.camera_owner = test_value
        self.assertEqual(self.instance.camera_owner, test_value)
    
    def test_owner_url_property(self):
        """
        Test owner_url property
        """
        test_value = 'stlscgpiodizsesmjzek'
        self.instance.owner_url = test_value
        self.assertEqual(self.instance.owner_url, test_value)
    
    def test_image_url_property(self):
        """
        Test image_url property
        """
        test_value = 'qedzllmsymugaagbcyoy'
        self.instance.image_url = test_value
        self.assertEqual(self.instance.image_url, test_value)
    
    def test_image_width_property(self):
        """
        Test image_width property
        """
        test_value = int(0)
        self.instance.image_width = test_value
        self.assertEqual(self.instance.image_width, test_value)
    
    def test_image_height_property(self):
        """
        Test image_height property
        """
        test_value = int(92)
        self.instance.image_height = test_value
        self.assertEqual(self.instance.image_height, test_value)
    
    def test_is_active_property(self):
        """
        Test is_active property
        """
        test_value = True
        self.instance.is_active = test_value
        self.assertEqual(self.instance.is_active, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'ohcwwsbldlrzebmqjrxj'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_sort_order_property(self):
        """
        Test sort_order property
        """
        test_value = int(31)
        self.instance.sort_order = test_value
        self.assertEqual(self.instance.sort_order, test_value)
    
    def test_display_latitude_property(self):
        """
        Test display_latitude property
        """
        test_value = float(92.2385517242461)
        self.instance.display_latitude = test_value
        self.assertEqual(self.instance.display_latitude, test_value)
    
    def test_display_longitude_property(self):
        """
        Test display_longitude property
        """
        test_value = float(85.08958042992533)
        self.instance.display_longitude = test_value
        self.assertEqual(self.instance.display_longitude, test_value)
    
    def test_location_description_property(self):
        """
        Test location_description property
        """
        test_value = 'labxvqinmjqyxjzidtqi'
        self.instance.location_description = test_value
        self.assertEqual(self.instance.location_description, test_value)
    
    def test_location_direction_property(self):
        """
        Test location_direction property
        """
        test_value = 'nmzwhfvuxouxurpsanyw'
        self.instance.location_direction = test_value
        self.assertEqual(self.instance.location_direction, test_value)
    
    def test_location_road_name_property(self):
        """
        Test location_road_name property
        """
        test_value = 'nngqetzlzftiikayqlch'
        self.instance.location_road_name = test_value
        self.assertEqual(self.instance.location_road_name, test_value)
    
    def test_location_milepost_property(self):
        """
        Test location_milepost property
        """
        test_value = float(66.68529093940218)
        self.instance.location_milepost = test_value
        self.assertEqual(self.instance.location_milepost, test_value)
    
    def test_location_latitude_property(self):
        """
        Test location_latitude property
        """
        test_value = float(46.869842349717686)
        self.instance.location_latitude = test_value
        self.assertEqual(self.instance.location_latitude, test_value)
    
    def test_location_longitude_property(self):
        """
        Test location_longitude property
        """
        test_value = float(64.08420685615083)
        self.instance.location_longitude = test_value
        self.assertEqual(self.instance.location_longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = HighwayCamera.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = HighwayCamera.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

