"""
Test case for Grid
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.de.dwd.icond2.grid import Grid


class Test_Grid(unittest.TestCase):
    """
    Test case for Grid
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Grid.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Grid for testing
        """
        instance = Grid(
            run_id='fbwxbhhdiylivoirxtjm',
            run_time='vpuejmrdahqhhuamdnhr',
            parameter='rrztexdawnogkvoprtqd',
            unit='ninijtcwhauzfctckolb',
            lead_hour=int(42),
            valid_time='mlekfqgyjccgxvjskcbx',
            produced_at='civrqaaikdrpgrrymnww',
            source_url='zptojjzmjooxtdrbgmhr',
            resolution_deg=float(57.489659757633014),
            bbox_min_lon=float(86.34681962440187),
            bbox_min_lat=float(99.49208569174088),
            bbox_max_lon=float(12.254348066598542),
            bbox_max_lat=float(38.58950624026703),
            lats=[float(39.92187281437259), float(43.721652771192396)],
            lons=[float(26.50590691509871)],
            values=[float(65.46033357057797)]
        )
        return instance

    
    def test_run_id_property(self):
        """
        Test run_id property
        """
        test_value = 'fbwxbhhdiylivoirxtjm'
        self.instance.run_id = test_value
        self.assertEqual(self.instance.run_id, test_value)
    
    def test_run_time_property(self):
        """
        Test run_time property
        """
        test_value = 'vpuejmrdahqhhuamdnhr'
        self.instance.run_time = test_value
        self.assertEqual(self.instance.run_time, test_value)
    
    def test_parameter_property(self):
        """
        Test parameter property
        """
        test_value = 'rrztexdawnogkvoprtqd'
        self.instance.parameter = test_value
        self.assertEqual(self.instance.parameter, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'ninijtcwhauzfctckolb'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_lead_hour_property(self):
        """
        Test lead_hour property
        """
        test_value = int(42)
        self.instance.lead_hour = test_value
        self.assertEqual(self.instance.lead_hour, test_value)
    
    def test_valid_time_property(self):
        """
        Test valid_time property
        """
        test_value = 'mlekfqgyjccgxvjskcbx'
        self.instance.valid_time = test_value
        self.assertEqual(self.instance.valid_time, test_value)
    
    def test_produced_at_property(self):
        """
        Test produced_at property
        """
        test_value = 'civrqaaikdrpgrrymnww'
        self.instance.produced_at = test_value
        self.assertEqual(self.instance.produced_at, test_value)
    
    def test_source_url_property(self):
        """
        Test source_url property
        """
        test_value = 'zptojjzmjooxtdrbgmhr'
        self.instance.source_url = test_value
        self.assertEqual(self.instance.source_url, test_value)
    
    def test_resolution_deg_property(self):
        """
        Test resolution_deg property
        """
        test_value = float(57.489659757633014)
        self.instance.resolution_deg = test_value
        self.assertEqual(self.instance.resolution_deg, test_value)
    
    def test_bbox_min_lon_property(self):
        """
        Test bbox_min_lon property
        """
        test_value = float(86.34681962440187)
        self.instance.bbox_min_lon = test_value
        self.assertEqual(self.instance.bbox_min_lon, test_value)
    
    def test_bbox_min_lat_property(self):
        """
        Test bbox_min_lat property
        """
        test_value = float(99.49208569174088)
        self.instance.bbox_min_lat = test_value
        self.assertEqual(self.instance.bbox_min_lat, test_value)
    
    def test_bbox_max_lon_property(self):
        """
        Test bbox_max_lon property
        """
        test_value = float(12.254348066598542)
        self.instance.bbox_max_lon = test_value
        self.assertEqual(self.instance.bbox_max_lon, test_value)
    
    def test_bbox_max_lat_property(self):
        """
        Test bbox_max_lat property
        """
        test_value = float(38.58950624026703)
        self.instance.bbox_max_lat = test_value
        self.assertEqual(self.instance.bbox_max_lat, test_value)
    
    def test_lats_property(self):
        """
        Test lats property
        """
        test_value = [float(39.92187281437259), float(43.721652771192396)]
        self.instance.lats = test_value
        self.assertEqual(self.instance.lats, test_value)
    
    def test_lons_property(self):
        """
        Test lons property
        """
        test_value = [float(26.50590691509871)]
        self.instance.lons = test_value
        self.assertEqual(self.instance.lons, test_value)
    
    def test_values_property(self):
        """
        Test values property
        """
        test_value = [float(65.46033357057797)]
        self.instance.values = test_value
        self.assertEqual(self.instance.values, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Grid.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Grid.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

