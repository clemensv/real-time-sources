"""
Test case for CommercialVehicleRestriction
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_mqtt_producer_data.us.wa.wsdot.cvrestrictions.commercialvehiclerestriction import CommercialVehicleRestriction


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
            state_route_id='qmcnvhlhobmeozjmoyok',
            bridge_number='aatogpagbjoxialiarom',
            bridge_name='kdldcbgpggzbicnhnfzz',
            location_name='obqvadpxpdbljqdnmwtb',
            location_description='vykutihhckvtavrayjek',
            latitude=float(31.538688265825996),
            longitude=float(17.329149355166816),
            state='chlbohynxmdfwmbdhfiq',
            restriction_type='xyzblyaygorrontwmbyy',
            vehicle_type='dscmsbjxthtycsieqxhr',
            restriction_weight_in_pounds=int(60),
            maximum_gross_vehicle_weight_in_pounds=int(36),
            restriction_height_in_inches=int(48),
            restriction_width_in_inches=int(56),
            restriction_length_in_inches=int(39),
            is_permanent_restriction=False,
            is_warning=False,
            is_detour_available=False,
            is_exceptions_allowed=False,
            restriction_comment='eyghxbctqlalzudeomjr',
            date_posted='mirrskevvgtzwbuhftlt',
            date_effective='eqmvbbyzwapsnradwkif',
            date_expires='yguflialkzfqndykeelb'
        )
        return instance

    
    def test_state_route_id_property(self):
        """
        Test state_route_id property
        """
        test_value = 'qmcnvhlhobmeozjmoyok'
        self.instance.state_route_id = test_value
        self.assertEqual(self.instance.state_route_id, test_value)
    
    def test_bridge_number_property(self):
        """
        Test bridge_number property
        """
        test_value = 'aatogpagbjoxialiarom'
        self.instance.bridge_number = test_value
        self.assertEqual(self.instance.bridge_number, test_value)
    
    def test_bridge_name_property(self):
        """
        Test bridge_name property
        """
        test_value = 'kdldcbgpggzbicnhnfzz'
        self.instance.bridge_name = test_value
        self.assertEqual(self.instance.bridge_name, test_value)
    
    def test_location_name_property(self):
        """
        Test location_name property
        """
        test_value = 'obqvadpxpdbljqdnmwtb'
        self.instance.location_name = test_value
        self.assertEqual(self.instance.location_name, test_value)
    
    def test_location_description_property(self):
        """
        Test location_description property
        """
        test_value = 'vykutihhckvtavrayjek'
        self.instance.location_description = test_value
        self.assertEqual(self.instance.location_description, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(31.538688265825996)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(17.329149355166816)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'chlbohynxmdfwmbdhfiq'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_restriction_type_property(self):
        """
        Test restriction_type property
        """
        test_value = 'xyzblyaygorrontwmbyy'
        self.instance.restriction_type = test_value
        self.assertEqual(self.instance.restriction_type, test_value)
    
    def test_vehicle_type_property(self):
        """
        Test vehicle_type property
        """
        test_value = 'dscmsbjxthtycsieqxhr'
        self.instance.vehicle_type = test_value
        self.assertEqual(self.instance.vehicle_type, test_value)
    
    def test_restriction_weight_in_pounds_property(self):
        """
        Test restriction_weight_in_pounds property
        """
        test_value = int(60)
        self.instance.restriction_weight_in_pounds = test_value
        self.assertEqual(self.instance.restriction_weight_in_pounds, test_value)
    
    def test_maximum_gross_vehicle_weight_in_pounds_property(self):
        """
        Test maximum_gross_vehicle_weight_in_pounds property
        """
        test_value = int(36)
        self.instance.maximum_gross_vehicle_weight_in_pounds = test_value
        self.assertEqual(self.instance.maximum_gross_vehicle_weight_in_pounds, test_value)
    
    def test_restriction_height_in_inches_property(self):
        """
        Test restriction_height_in_inches property
        """
        test_value = int(48)
        self.instance.restriction_height_in_inches = test_value
        self.assertEqual(self.instance.restriction_height_in_inches, test_value)
    
    def test_restriction_width_in_inches_property(self):
        """
        Test restriction_width_in_inches property
        """
        test_value = int(56)
        self.instance.restriction_width_in_inches = test_value
        self.assertEqual(self.instance.restriction_width_in_inches, test_value)
    
    def test_restriction_length_in_inches_property(self):
        """
        Test restriction_length_in_inches property
        """
        test_value = int(39)
        self.instance.restriction_length_in_inches = test_value
        self.assertEqual(self.instance.restriction_length_in_inches, test_value)
    
    def test_is_permanent_restriction_property(self):
        """
        Test is_permanent_restriction property
        """
        test_value = False
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
        test_value = 'eyghxbctqlalzudeomjr'
        self.instance.restriction_comment = test_value
        self.assertEqual(self.instance.restriction_comment, test_value)
    
    def test_date_posted_property(self):
        """
        Test date_posted property
        """
        test_value = 'mirrskevvgtzwbuhftlt'
        self.instance.date_posted = test_value
        self.assertEqual(self.instance.date_posted, test_value)
    
    def test_date_effective_property(self):
        """
        Test date_effective property
        """
        test_value = 'eqmvbbyzwapsnradwkif'
        self.instance.date_effective = test_value
        self.assertEqual(self.instance.date_effective, test_value)
    
    def test_date_expires_property(self):
        """
        Test date_expires property
        """
        test_value = 'yguflialkzfqndykeelb'
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

