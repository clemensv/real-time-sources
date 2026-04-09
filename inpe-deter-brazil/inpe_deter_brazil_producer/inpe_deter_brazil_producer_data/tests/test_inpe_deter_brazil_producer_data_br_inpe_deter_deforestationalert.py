"""
Test case for DeforestationAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from inpe_deter_brazil_producer_data.br.inpe.deter.deforestationalert import DeforestationAlert


class Test_DeforestationAlert(unittest.TestCase):
    """
    Test case for DeforestationAlert
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DeforestationAlert.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DeforestationAlert for testing
        """
        instance = DeforestationAlert(
            alert_id='jilroravvpfslwtyygov',
            biome='jrtlmkmozebxzzahuehl',
            classname='bgdggzprpyonogvctllt',
            view_date='nevnoarvfoztcvwfbsah',
            satellite='woadmmhhyzguquswqlqv',
            sensor='ikbsqljryiqqwgnjyxsx',
            area_km2=float(74.73723847422322),
            municipality='zdklfouvfrujchfwjnmn',
            state_code='bpxbmczocenyhhwgehgd',
            path_row='cysuqqzypdlogaojfqsa',
            publish_month='ijtloqpjylubbgxezxni',
            centroid_latitude=float(76.84317730305523),
            centroid_longitude=float(57.65981899208311)
        )
        return instance

    
    def test_alert_id_property(self):
        """
        Test alert_id property
        """
        test_value = 'jilroravvpfslwtyygov'
        self.instance.alert_id = test_value
        self.assertEqual(self.instance.alert_id, test_value)
    
    def test_biome_property(self):
        """
        Test biome property
        """
        test_value = 'jrtlmkmozebxzzahuehl'
        self.instance.biome = test_value
        self.assertEqual(self.instance.biome, test_value)
    
    def test_classname_property(self):
        """
        Test classname property
        """
        test_value = 'bgdggzprpyonogvctllt'
        self.instance.classname = test_value
        self.assertEqual(self.instance.classname, test_value)
    
    def test_view_date_property(self):
        """
        Test view_date property
        """
        test_value = 'nevnoarvfoztcvwfbsah'
        self.instance.view_date = test_value
        self.assertEqual(self.instance.view_date, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = 'woadmmhhyzguquswqlqv'
        self.instance.satellite = test_value
        self.assertEqual(self.instance.satellite, test_value)
    
    def test_sensor_property(self):
        """
        Test sensor property
        """
        test_value = 'ikbsqljryiqqwgnjyxsx'
        self.instance.sensor = test_value
        self.assertEqual(self.instance.sensor, test_value)
    
    def test_area_km2_property(self):
        """
        Test area_km2 property
        """
        test_value = float(74.73723847422322)
        self.instance.area_km2 = test_value
        self.assertEqual(self.instance.area_km2, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'zdklfouvfrujchfwjnmn'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_state_code_property(self):
        """
        Test state_code property
        """
        test_value = 'bpxbmczocenyhhwgehgd'
        self.instance.state_code = test_value
        self.assertEqual(self.instance.state_code, test_value)
    
    def test_path_row_property(self):
        """
        Test path_row property
        """
        test_value = 'cysuqqzypdlogaojfqsa'
        self.instance.path_row = test_value
        self.assertEqual(self.instance.path_row, test_value)
    
    def test_publish_month_property(self):
        """
        Test publish_month property
        """
        test_value = 'ijtloqpjylubbgxezxni'
        self.instance.publish_month = test_value
        self.assertEqual(self.instance.publish_month, test_value)
    
    def test_centroid_latitude_property(self):
        """
        Test centroid_latitude property
        """
        test_value = float(76.84317730305523)
        self.instance.centroid_latitude = test_value
        self.assertEqual(self.instance.centroid_latitude, test_value)
    
    def test_centroid_longitude_property(self):
        """
        Test centroid_longitude property
        """
        test_value = float(57.65981899208311)
        self.instance.centroid_longitude = test_value
        self.assertEqual(self.instance.centroid_longitude, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DeforestationAlert.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
