"""
Test case for VolcanicEruption
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_volcano_producer_data.volcaniceruption import VolcanicEruption
from jma_bosai_volcano_producer_data.eruptiontypeenum import EruptionTypeenum
import datetime


class Test_VolcanicEruption(unittest.TestCase):
    """
    Test case for VolcanicEruption
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VolcanicEruption.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VolcanicEruption for testing
        """
        instance = VolcanicEruption(
            volcano_code='sextdjqvlqkbyjhuwoev',
            event_id='lokiopwahzwnqlhmijfe',
            report_datetime=datetime.datetime.now(datetime.timezone.utc),
            report_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            eruption_datetime=datetime.datetime.now(datetime.timezone.utc),
            eruption_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            eruption_type=EruptionTypeenum.ERUPTION,
            crater_name='wgzgaabbxzkgsnbbusbt',
            colored_plume_height_m=float(95.40343712953083),
            white_plume_height_m=float(3.870844857220035),
            maximum_plume_height_since_start_m=float(20.187355114430783),
            plume_direction='wmmtijteecmregbrqsge',
            ash_dispersal_direction='lxreqynzbxqouxjuymiq',
            pyroclastic_flow_observed=True,
            plume_amount_jp='eajjfvhljxoyosyytehp',
            description='uaiskjoqfvqhavnfrowi',
            info_type_jp='qfsoidkkdjpwciyxrnqc',
            area_codes=['mtrsiziaasovmnnkspnb', 'arxewxnebksdfebflszc', 'bskirjqsupufqjcarzzh', 'tcjdkaminhdqetfpcuni', 'ogssbdxfrmvtpqmqythm']
        )
        return instance

    
    def test_volcano_code_property(self):
        """
        Test volcano_code property
        """
        test_value = 'sextdjqvlqkbyjhuwoev'
        self.instance.volcano_code = test_value
        self.assertEqual(self.instance.volcano_code, test_value)
    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'lokiopwahzwnqlhmijfe'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_report_datetime_property(self):
        """
        Test report_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.report_datetime = test_value
        self.assertEqual(self.instance.report_datetime, test_value)
    
    def test_report_datetime_local_property(self):
        """
        Test report_datetime_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.report_datetime_local = test_value
        self.assertEqual(self.instance.report_datetime_local, test_value)
    
    def test_eruption_datetime_property(self):
        """
        Test eruption_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.eruption_datetime = test_value
        self.assertEqual(self.instance.eruption_datetime, test_value)
    
    def test_eruption_datetime_local_property(self):
        """
        Test eruption_datetime_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.eruption_datetime_local = test_value
        self.assertEqual(self.instance.eruption_datetime_local, test_value)
    
    def test_eruption_type_property(self):
        """
        Test eruption_type property
        """
        test_value = EruptionTypeenum.ERUPTION
        self.instance.eruption_type = test_value
        self.assertEqual(self.instance.eruption_type, test_value)
    
    def test_crater_name_property(self):
        """
        Test crater_name property
        """
        test_value = 'wgzgaabbxzkgsnbbusbt'
        self.instance.crater_name = test_value
        self.assertEqual(self.instance.crater_name, test_value)
    
    def test_colored_plume_height_m_property(self):
        """
        Test colored_plume_height_m property
        """
        test_value = float(95.40343712953083)
        self.instance.colored_plume_height_m = test_value
        self.assertEqual(self.instance.colored_plume_height_m, test_value)
    
    def test_white_plume_height_m_property(self):
        """
        Test white_plume_height_m property
        """
        test_value = float(3.870844857220035)
        self.instance.white_plume_height_m = test_value
        self.assertEqual(self.instance.white_plume_height_m, test_value)
    
    def test_maximum_plume_height_since_start_m_property(self):
        """
        Test maximum_plume_height_since_start_m property
        """
        test_value = float(20.187355114430783)
        self.instance.maximum_plume_height_since_start_m = test_value
        self.assertEqual(self.instance.maximum_plume_height_since_start_m, test_value)
    
    def test_plume_direction_property(self):
        """
        Test plume_direction property
        """
        test_value = 'wmmtijteecmregbrqsge'
        self.instance.plume_direction = test_value
        self.assertEqual(self.instance.plume_direction, test_value)
    
    def test_ash_dispersal_direction_property(self):
        """
        Test ash_dispersal_direction property
        """
        test_value = 'lxreqynzbxqouxjuymiq'
        self.instance.ash_dispersal_direction = test_value
        self.assertEqual(self.instance.ash_dispersal_direction, test_value)
    
    def test_pyroclastic_flow_observed_property(self):
        """
        Test pyroclastic_flow_observed property
        """
        test_value = True
        self.instance.pyroclastic_flow_observed = test_value
        self.assertEqual(self.instance.pyroclastic_flow_observed, test_value)
    
    def test_plume_amount_jp_property(self):
        """
        Test plume_amount_jp property
        """
        test_value = 'eajjfvhljxoyosyytehp'
        self.instance.plume_amount_jp = test_value
        self.assertEqual(self.instance.plume_amount_jp, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'uaiskjoqfvqhavnfrowi'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_info_type_jp_property(self):
        """
        Test info_type_jp property
        """
        test_value = 'qfsoidkkdjpwciyxrnqc'
        self.instance.info_type_jp = test_value
        self.assertEqual(self.instance.info_type_jp, test_value)
    
    def test_area_codes_property(self):
        """
        Test area_codes property
        """
        test_value = ['mtrsiziaasovmnnkspnb', 'arxewxnebksdfebflszc', 'bskirjqsupufqjcarzzh', 'tcjdkaminhdqetfpcuni', 'ogssbdxfrmvtpqmqythm']
        self.instance.area_codes = test_value
        self.assertEqual(self.instance.area_codes, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VolcanicEruption.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VolcanicEruption.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

