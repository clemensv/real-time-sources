"""
Test case for CommercialVehicleRestriction
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_amqp_producer_data.us.wa.wsdot.cvrestrictions.commercialvehiclerestriction import CommercialVehicleRestriction


class Test_CommercialVehicleRestriction(unittest.TestCase):
    """
    Test case for CommercialVehicleRestriction
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CommercialVehicleRestriction.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CommercialVehicleRestriction for testing
        """
        instance = CommercialVehicleRestriction(
            state_route_id='hphfaqutqfuamwetugqo',
            bridge_number='dpqxcqhydmuklftowfzg',
            bridge_name='mmmjewbfpbszaftdgfkx',
            location_name='podsjvsokxfrsygfcrjg',
            location_description='cuaitqnzrttbnzijhmpj',
            latitude=float(17.80835884773956),
            longitude=float(42.027700040413706),
            state='hbjizirjgtorcfylpwyx',
            restriction_type='fnymtbiulekucpqfzdfv',
            vehicle_type='sthqytnjtyqkmkmudemh',
            restriction_weight_in_pounds=int(68),
            maximum_gross_vehicle_weight_in_pounds=int(30),
            restriction_height_in_inches=int(53),
            restriction_width_in_inches=int(39),
            restriction_length_in_inches=int(78),
            is_permanent_restriction=True,
            is_warning=False,
            is_detour_available=False,
            is_exceptions_allowed=False,
            restriction_comment='ikjpqsexhvnbzxsizygq',
            date_posted='eulsoemgawgcahbnmhvy',
            date_effective='gullzymfjowiteqkegqv',
            date_expires='xmjjykeesiyblhnsfble'
        )
        return instance

    
    def test_state_route_id_property(self):
        """
        Test state_route_id property
        """
        test_value = 'hphfaqutqfuamwetugqo'
        self.instance.state_route_id = test_value
        self.assertEqual(self.instance.state_route_id, test_value)
    
    def test_bridge_number_property(self):
        """
        Test bridge_number property
        """
        test_value = 'dpqxcqhydmuklftowfzg'
        self.instance.bridge_number = test_value
        self.assertEqual(self.instance.bridge_number, test_value)
    
    def test_bridge_name_property(self):
        """
        Test bridge_name property
        """
        test_value = 'mmmjewbfpbszaftdgfkx'
        self.instance.bridge_name = test_value
        self.assertEqual(self.instance.bridge_name, test_value)
    
    def test_location_name_property(self):
        """
        Test location_name property
        """
        test_value = 'podsjvsokxfrsygfcrjg'
        self.instance.location_name = test_value
        self.assertEqual(self.instance.location_name, test_value)
    
    def test_location_description_property(self):
        """
        Test location_description property
        """
        test_value = 'cuaitqnzrttbnzijhmpj'
        self.instance.location_description = test_value
        self.assertEqual(self.instance.location_description, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(17.80835884773956)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(42.027700040413706)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'hbjizirjgtorcfylpwyx'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_restriction_type_property(self):
        """
        Test restriction_type property
        """
        test_value = 'fnymtbiulekucpqfzdfv'
        self.instance.restriction_type = test_value
        self.assertEqual(self.instance.restriction_type, test_value)
    
    def test_vehicle_type_property(self):
        """
        Test vehicle_type property
        """
        test_value = 'sthqytnjtyqkmkmudemh'
        self.instance.vehicle_type = test_value
        self.assertEqual(self.instance.vehicle_type, test_value)
    
    def test_restriction_weight_in_pounds_property(self):
        """
        Test restriction_weight_in_pounds property
        """
        test_value = int(68)
        self.instance.restriction_weight_in_pounds = test_value
        self.assertEqual(self.instance.restriction_weight_in_pounds, test_value)
    
    def test_maximum_gross_vehicle_weight_in_pounds_property(self):
        """
        Test maximum_gross_vehicle_weight_in_pounds property
        """
        test_value = int(30)
        self.instance.maximum_gross_vehicle_weight_in_pounds = test_value
        self.assertEqual(self.instance.maximum_gross_vehicle_weight_in_pounds, test_value)
    
    def test_restriction_height_in_inches_property(self):
        """
        Test restriction_height_in_inches property
        """
        test_value = int(53)
        self.instance.restriction_height_in_inches = test_value
        self.assertEqual(self.instance.restriction_height_in_inches, test_value)
    
    def test_restriction_width_in_inches_property(self):
        """
        Test restriction_width_in_inches property
        """
        test_value = int(39)
        self.instance.restriction_width_in_inches = test_value
        self.assertEqual(self.instance.restriction_width_in_inches, test_value)
    
    def test_restriction_length_in_inches_property(self):
        """
        Test restriction_length_in_inches property
        """
        test_value = int(78)
        self.instance.restriction_length_in_inches = test_value
        self.assertEqual(self.instance.restriction_length_in_inches, test_value)
    
    def test_is_permanent_restriction_property(self):
        """
        Test is_permanent_restriction property
        """
        test_value = True
        self.instance.is_permanent_restriction = test_value
        self.assertEqual(self.instance.is_permanent_restriction, test_value)
    
    def test_is_warning_property(self):
        """
        Test is_warning property
        """
        test_value = False
        self.instance.is_warning = test_value
        self.assertEqual(self.instance.is_warning, test_value)
    
    def test_is_detour_available_property(self):
        """
        Test is_detour_available property
        """
        test_value = False
        self.instance.is_detour_available = test_value
        self.assertEqual(self.instance.is_detour_available, test_value)
    
    def test_is_exceptions_allowed_property(self):
        """
        Test is_exceptions_allowed property
        """
        test_value = False
        self.instance.is_exceptions_allowed = test_value
        self.assertEqual(self.instance.is_exceptions_allowed, test_value)
    
    def test_restriction_comment_property(self):
        """
        Test restriction_comment property
        """
        test_value = 'ikjpqsexhvnbzxsizygq'
        self.instance.restriction_comment = test_value
        self.assertEqual(self.instance.restriction_comment, test_value)
    
    def test_date_posted_property(self):
        """
        Test date_posted property
        """
        test_value = 'eulsoemgawgcahbnmhvy'
        self.instance.date_posted = test_value
        self.assertEqual(self.instance.date_posted, test_value)
    
    def test_date_effective_property(self):
        """
        Test date_effective property
        """
        test_value = 'gullzymfjowiteqkegqv'
        self.instance.date_effective = test_value
        self.assertEqual(self.instance.date_effective, test_value)
    
    def test_date_expires_property(self):
        """
        Test date_expires property
        """
        test_value = 'xmjjykeesiyblhnsfble'
        self.instance.date_expires = test_value
        self.assertEqual(self.instance.date_expires, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CommercialVehicleRestriction.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = CommercialVehicleRestriction.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

