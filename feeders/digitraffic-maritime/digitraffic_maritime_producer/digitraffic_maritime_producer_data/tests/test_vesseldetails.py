"""
Test case for VesselDetails
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.vesseldetails import VesselDetails
from digitraffic_maritime_producer_data.vesseldimensions import VesselDimensions
from digitraffic_maritime_producer_data.vesselregistration import VesselRegistration
from digitraffic_maritime_producer_data.vesselconstruction import VesselConstruction
from digitraffic_maritime_producer_data.vesselsystem import VesselSystem
import datetime


class Test_VesselDetails(unittest.TestCase):
    """
    Test case for VesselDetails
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VesselDetails.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VesselDetails for testing
        """
        instance = VesselDetails(
            vessel_id=int(38),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
            mmsi=int(86),
            name='kdscrbpclhgicigudmjr',
            name_prefix='lgglpjrkfjgstmegmksd',
            imo_lloyds=int(38),
            radio_call_sign='ivydhizbfuwneizezied',
            radio_call_sign_type='skeegephvjsurhpkqzah',
            data_source='ljbuxdfanbryvxejvrzx',
            vessel_construction=None,
            vessel_dimensions=None,
            vessel_registration=None,
            vessel_system=None
        )
        return instance

    
    def test_vessel_id_property(self):
        """
        Test vessel_id property
        """
        test_value = int(38)
        self.instance.vessel_id = test_value
        self.assertEqual(self.instance.vessel_id, test_value)
    
    def test_updated_at_property(self):
        """
        Test updated_at property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.updated_at = test_value
        self.assertEqual(self.instance.updated_at, test_value)
    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(86)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'kdscrbpclhgicigudmjr'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_name_prefix_property(self):
        """
        Test name_prefix property
        """
        test_value = 'lgglpjrkfjgstmegmksd'
        self.instance.name_prefix = test_value
        self.assertEqual(self.instance.name_prefix, test_value)
    
    def test_imo_lloyds_property(self):
        """
        Test imo_lloyds property
        """
        test_value = int(38)
        self.instance.imo_lloyds = test_value
        self.assertEqual(self.instance.imo_lloyds, test_value)
    
    def test_radio_call_sign_property(self):
        """
        Test radio_call_sign property
        """
        test_value = 'ivydhizbfuwneizezied'
        self.instance.radio_call_sign = test_value
        self.assertEqual(self.instance.radio_call_sign, test_value)
    
    def test_radio_call_sign_type_property(self):
        """
        Test radio_call_sign_type property
        """
        test_value = 'skeegephvjsurhpkqzah'
        self.instance.radio_call_sign_type = test_value
        self.assertEqual(self.instance.radio_call_sign_type, test_value)
    
    def test_data_source_property(self):
        """
        Test data_source property
        """
        test_value = 'ljbuxdfanbryvxejvrzx'
        self.instance.data_source = test_value
        self.assertEqual(self.instance.data_source, test_value)
    
    def test_vessel_construction_property(self):
        """
        Test vessel_construction property
        """
        test_value = None
        self.instance.vessel_construction = test_value
        self.assertEqual(self.instance.vessel_construction, test_value)
    
    def test_vessel_dimensions_property(self):
        """
        Test vessel_dimensions property
        """
        test_value = None
        self.instance.vessel_dimensions = test_value
        self.assertEqual(self.instance.vessel_dimensions, test_value)
    
    def test_vessel_registration_property(self):
        """
        Test vessel_registration property
        """
        test_value = None
        self.instance.vessel_registration = test_value
        self.assertEqual(self.instance.vessel_registration, test_value)
    
    def test_vessel_system_property(self):
        """
        Test vessel_system property
        """
        test_value = None
        self.instance.vessel_system = test_value
        self.assertEqual(self.instance.vessel_system, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VesselDetails.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VesselDetails.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

