"""
Test case for DeforestationAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from inpe_deter_brazil_amqp_producer_data.br.inpe.deter.deforestationalert import DeforestationAlert
from inpe_deter_brazil_amqp_producer_data.br.inpe.deter.classslugenum import ClassSlugenum
from inpe_deter_brazil_amqp_producer_data.br.inpe.deter.biomeenum import BiomeEnum


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
            alert_id='iwralkmczczcaantstrm',
            biome=BiomeEnum.amazon,
            classname='qmttghqhxkloikcfbahq',
            view_date='frrvzuvunezspjepmhqt',
            satellite='jbdycvqebtkglranyxph',
            sensor='nbukoypdnlhwqtezuwuf',
            area_km2=float(16.06261146697765),
            municipality='fqghmbztyrdopywwmqmd',
            state_code='pxakpvjthffujowleaay',
            path_row='bdtbbreossnofgncsfif',
            publish_month='pdjjovytamhnghcpysat',
            centroid_latitude=float(52.0016613547302),
            centroid_longitude=float(41.84596385171342),
            state_slug='mwvrfzmuhfjkofiqrdzz',
            class_slug=ClassSlugenum.desmatamento_cr
        )
        return instance

    
    def test_alert_id_property(self):
        """
        Test alert_id property
        """
        test_value = 'iwralkmczczcaantstrm'
        self.instance.alert_id = test_value
        self.assertEqual(self.instance.alert_id, test_value)
    
    def test_biome_property(self):
        """
        Test biome property
        """
        test_value = BiomeEnum.amazon
        self.instance.biome = test_value
        self.assertEqual(self.instance.biome, test_value)
    
    def test_classname_property(self):
        """
        Test classname property
        """
        test_value = 'qmttghqhxkloikcfbahq'
        self.instance.classname = test_value
        self.assertEqual(self.instance.classname, test_value)
    
    def test_view_date_property(self):
        """
        Test view_date property
        """
        test_value = 'frrvzuvunezspjepmhqt'
        self.instance.view_date = test_value
        self.assertEqual(self.instance.view_date, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = 'jbdycvqebtkglranyxph'
        self.instance.satellite = test_value
        self.assertEqual(self.instance.satellite, test_value)
    
    def test_sensor_property(self):
        """
        Test sensor property
        """
        test_value = 'nbukoypdnlhwqtezuwuf'
        self.instance.sensor = test_value
        self.assertEqual(self.instance.sensor, test_value)
    
    def test_area_km2_property(self):
        """
        Test area_km2 property
        """
        test_value = float(16.06261146697765)
        self.instance.area_km2 = test_value
        self.assertEqual(self.instance.area_km2, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'fqghmbztyrdopywwmqmd'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_state_code_property(self):
        """
        Test state_code property
        """
        test_value = 'pxakpvjthffujowleaay'
        self.instance.state_code = test_value
        self.assertEqual(self.instance.state_code, test_value)
    
    def test_path_row_property(self):
        """
        Test path_row property
        """
        test_value = 'bdtbbreossnofgncsfif'
        self.instance.path_row = test_value
        self.assertEqual(self.instance.path_row, test_value)
    
    def test_publish_month_property(self):
        """
        Test publish_month property
        """
        test_value = 'pdjjovytamhnghcpysat'
        self.instance.publish_month = test_value
        self.assertEqual(self.instance.publish_month, test_value)
    
    def test_centroid_latitude_property(self):
        """
        Test centroid_latitude property
        """
        test_value = float(52.0016613547302)
        self.instance.centroid_latitude = test_value
        self.assertEqual(self.instance.centroid_latitude, test_value)
    
    def test_centroid_longitude_property(self):
        """
        Test centroid_longitude property
        """
        test_value = float(41.84596385171342)
        self.instance.centroid_longitude = test_value
        self.assertEqual(self.instance.centroid_longitude, test_value)
    
    def test_state_slug_property(self):
        """
        Test state_slug property
        """
        test_value = 'mwvrfzmuhfjkofiqrdzz'
        self.instance.state_slug = test_value
        self.assertEqual(self.instance.state_slug, test_value)
    
    def test_class_slug_property(self):
        """
        Test class_slug property
        """
        test_value = ClassSlugenum.desmatamento_cr
        self.instance.class_slug = test_value
        self.assertEqual(self.instance.class_slug, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DeforestationAlert.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DeforestationAlert.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

