"""
Test case for RoadEvent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.roadevent import RoadEvent


class Test_RoadEvent(unittest.TestCase):
    """
    Test case for RoadEvent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RoadEvent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RoadEvent for testing
        """
        instance = RoadEvent(
            situation_id='pudrajygwkcezdrrvngr',
            record_id='ilbmsqqoxhjzdlpnxyjs',
            version='uxeswdrifzsatsodovsc',
            severity='hifxdrwxxayxbcuvguvi',
            record_type='qdmcpehvjcpzlljeeiof',
            probability='xstoepaqpeyhefjobqir',
            latitude=float(79.6630498754166),
            longitude=float(1.1492085328507207),
            road_number='ecmcprauylqibvylvgxn',
            town_name='wodvnozqjwskapvjqjdp',
            direction='asxulpvzbdwpdiczwaev',
            description='jrfliihfqcldmiveddlo',
            location_description='ijwhmgipvnyzxokqqfng',
            source_name='zoyfqgquunbfbyltxxti',
            validity_status='hgndohppefawbjnavxwe',
            overall_start_time='edalxwnrpdrasfkpazhl',
            overall_end_time='myaawagpwsilrzblkrwb',
            creation_time='wuodmsuvwmzarhlnyxpv',
            observation_time='akdrpxqvzmkldzsqcwdo'
        )
        return instance

    
    def test_situation_id_property(self):
        """
        Test situation_id property
        """
        test_value = 'pudrajygwkcezdrrvngr'
        self.instance.situation_id = test_value
        self.assertEqual(self.instance.situation_id, test_value)
    
    def test_record_id_property(self):
        """
        Test record_id property
        """
        test_value = 'ilbmsqqoxhjzdlpnxyjs'
        self.instance.record_id = test_value
        self.assertEqual(self.instance.record_id, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = 'uxeswdrifzsatsodovsc'
        self.instance.version = test_value
        self.assertEqual(self.instance.version, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'hifxdrwxxayxbcuvguvi'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_record_type_property(self):
        """
        Test record_type property
        """
        test_value = 'qdmcpehvjcpzlljeeiof'
        self.instance.record_type = test_value
        self.assertEqual(self.instance.record_type, test_value)
    
    def test_probability_property(self):
        """
        Test probability property
        """
        test_value = 'xstoepaqpeyhefjobqir'
        self.instance.probability = test_value
        self.assertEqual(self.instance.probability, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(79.6630498754166)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(1.1492085328507207)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_road_number_property(self):
        """
        Test road_number property
        """
        test_value = 'ecmcprauylqibvylvgxn'
        self.instance.road_number = test_value
        self.assertEqual(self.instance.road_number, test_value)
    
    def test_town_name_property(self):
        """
        Test town_name property
        """
        test_value = 'wodvnozqjwskapvjqjdp'
        self.instance.town_name = test_value
        self.assertEqual(self.instance.town_name, test_value)
    
    def test_direction_property(self):
        """
        Test direction property
        """
        test_value = 'asxulpvzbdwpdiczwaev'
        self.instance.direction = test_value
        self.assertEqual(self.instance.direction, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'jrfliihfqcldmiveddlo'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_location_description_property(self):
        """
        Test location_description property
        """
        test_value = 'ijwhmgipvnyzxokqqfng'
        self.instance.location_description = test_value
        self.assertEqual(self.instance.location_description, test_value)
    
    def test_source_name_property(self):
        """
        Test source_name property
        """
        test_value = 'zoyfqgquunbfbyltxxti'
        self.instance.source_name = test_value
        self.assertEqual(self.instance.source_name, test_value)
    
    def test_validity_status_property(self):
        """
        Test validity_status property
        """
        test_value = 'hgndohppefawbjnavxwe'
        self.instance.validity_status = test_value
        self.assertEqual(self.instance.validity_status, test_value)
    
    def test_overall_start_time_property(self):
        """
        Test overall_start_time property
        """
        test_value = 'edalxwnrpdrasfkpazhl'
        self.instance.overall_start_time = test_value
        self.assertEqual(self.instance.overall_start_time, test_value)
    
    def test_overall_end_time_property(self):
        """
        Test overall_end_time property
        """
        test_value = 'myaawagpwsilrzblkrwb'
        self.instance.overall_end_time = test_value
        self.assertEqual(self.instance.overall_end_time, test_value)
    
    def test_creation_time_property(self):
        """
        Test creation_time property
        """
        test_value = 'wuodmsuvwmzarhlnyxpv'
        self.instance.creation_time = test_value
        self.assertEqual(self.instance.creation_time, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'akdrpxqvzmkldzsqcwdo'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RoadEvent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
