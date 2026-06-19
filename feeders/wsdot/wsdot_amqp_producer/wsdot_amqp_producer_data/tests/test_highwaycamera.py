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
            camera_id='nzubiolfpemdwbjcdsuk',
            title='enurplsjzxywjzxlcenz',
            description='shqzyawqehllqfkbpftf',
            camera_owner='gwgbpxapczgzlvsuynfn',
            owner_url='arncgnqrawxipqstgxpv',
            image_url='azdnrkcntnyxvyvsjrhm',
            image_width=int(19),
            image_height=int(63),
            is_active=True,
            region='gfevsmftuarmjqhiufuo',
            sort_order=int(53),
            display_latitude=float(15.58653852390275),
            display_longitude=float(26.38778711941947),
            location_description='tndftoclkkgkqbmnrtev',
            location_direction='cbggarubgzxsfuveutue',
            location_road_name='ayvcdwcwhybevewnraoi',
            location_milepost=float(94.59157254869423),
            location_latitude=float(34.28176748146519),
            location_longitude=float(55.01585475952551)
        )
        return instance

    
    def test_camera_id_property(self):
        """
        Test camera_id property
        """
        test_value = 'nzubiolfpemdwbjcdsuk'
        self.instance.camera_id = test_value
        self.assertEqual(self.instance.camera_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'enurplsjzxywjzxlcenz'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'shqzyawqehllqfkbpftf'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_camera_owner_property(self):
        """
        Test camera_owner property
        """
        test_value = 'gwgbpxapczgzlvsuynfn'
        self.instance.camera_owner = test_value
        self.assertEqual(self.instance.camera_owner, test_value)
    
    def test_owner_url_property(self):
        """
        Test owner_url property
        """
        test_value = 'arncgnqrawxipqstgxpv'
        self.instance.owner_url = test_value
        self.assertEqual(self.instance.owner_url, test_value)
    
    def test_image_url_property(self):
        """
        Test image_url property
        """
        test_value = 'azdnrkcntnyxvyvsjrhm'
        self.instance.image_url = test_value
        self.assertEqual(self.instance.image_url, test_value)
    
    def test_image_width_property(self):
        """
        Test image_width property
        """
        test_value = int(19)
        self.instance.image_width = test_value
        self.assertEqual(self.instance.image_width, test_value)
    
    def test_image_height_property(self):
        """
        Test image_height property
        """
        test_value = int(63)
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
        test_value = 'gfevsmftuarmjqhiufuo'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_sort_order_property(self):
        """
        Test sort_order property
        """
        test_value = int(53)
        self.instance.sort_order = test_value
        self.assertEqual(self.instance.sort_order, test_value)
    
    def test_display_latitude_property(self):
        """
        Test display_latitude property
        """
        test_value = float(15.58653852390275)
        self.instance.display_latitude = test_value
        self.assertEqual(self.instance.display_latitude, test_value)
    
    def test_display_longitude_property(self):
        """
        Test display_longitude property
        """
        test_value = float(26.38778711941947)
        self.instance.display_longitude = test_value
        self.assertEqual(self.instance.display_longitude, test_value)
    
    def test_location_description_property(self):
        """
        Test location_description property
        """
        test_value = 'tndftoclkkgkqbmnrtev'
        self.instance.location_description = test_value
        self.assertEqual(self.instance.location_description, test_value)
    
    def test_location_direction_property(self):
        """
        Test location_direction property
        """
        test_value = 'cbggarubgzxsfuveutue'
        self.instance.location_direction = test_value
        self.assertEqual(self.instance.location_direction, test_value)
    
    def test_location_road_name_property(self):
        """
        Test location_road_name property
        """
        test_value = 'ayvcdwcwhybevewnraoi'
        self.instance.location_road_name = test_value
        self.assertEqual(self.instance.location_road_name, test_value)
    
    def test_location_milepost_property(self):
        """
        Test location_milepost property
        """
        test_value = float(94.59157254869423)
        self.instance.location_milepost = test_value
        self.assertEqual(self.instance.location_milepost, test_value)
    
    def test_location_latitude_property(self):
        """
        Test location_latitude property
        """
        test_value = float(34.28176748146519)
        self.instance.location_latitude = test_value
        self.assertEqual(self.instance.location_latitude, test_value)
    
    def test_location_longitude_property(self):
        """
        Test location_longitude property
        """
        test_value = float(55.01585475952551)
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

