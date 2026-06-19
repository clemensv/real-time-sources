"""
Test case for DeforestationAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from inpe_deter_brazil_producer_data.br.inpe.deter.deforestationalert import DeforestationAlert
from inpe_deter_brazil_producer_data.br.inpe.deter.biomeenum import BiomeEnum
from inpe_deter_brazil_producer_data.br.inpe.deter.classslugenum import ClassSlugenum


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
            alert_id='irggqgreigdguuurcqvm',
            biome=BiomeEnum.amazon,
            classname='phmylacsijmxjrphmkaq',
            view_date='ixgbbkwdkufrdchegiph',
            satellite='mpfaqynlxrxhtjukuxie',
            sensor='dglvfieoddmpiiemjylv',
            area_km2=float(28.64838145897306),
            municipality='ronpucybxgqvugcuarkk',
            state_code='sulizzdymdvchnnmtzin',
            path_row='rtrquykdsacvshzstdbv',
            publish_month='hlbprexeeihqcbfhdvbw',
            centroid_latitude=float(77.85751710385298),
            centroid_longitude=float(67.01249009092516),
            state_slug='xumrirtfmxaydgmppbvc',
            class_slug=ClassSlugenum.desmatamento_MINUScr
        )
        return instance

    
    def test_alert_id_property(self):
        """
        Test alert_id property
        """
        test_value = 'irggqgreigdguuurcqvm'
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
        test_value = 'phmylacsijmxjrphmkaq'
        self.instance.classname = test_value
        self.assertEqual(self.instance.classname, test_value)
    
    def test_view_date_property(self):
        """
        Test view_date property
        """
        test_value = 'ixgbbkwdkufrdchegiph'
        self.instance.view_date = test_value
        self.assertEqual(self.instance.view_date, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = 'mpfaqynlxrxhtjukuxie'
        self.instance.satellite = test_value
        self.assertEqual(self.instance.satellite, test_value)
    
    def test_sensor_property(self):
        """
        Test sensor property
        """
        test_value = 'dglvfieoddmpiiemjylv'
        self.instance.sensor = test_value
        self.assertEqual(self.instance.sensor, test_value)
    
    def test_area_km2_property(self):
        """
        Test area_km2 property
        """
        test_value = float(28.64838145897306)
        self.instance.area_km2 = test_value
        self.assertEqual(self.instance.area_km2, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'ronpucybxgqvugcuarkk'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_state_code_property(self):
        """
        Test state_code property
        """
        test_value = 'sulizzdymdvchnnmtzin'
        self.instance.state_code = test_value
        self.assertEqual(self.instance.state_code, test_value)
    
    def test_path_row_property(self):
        """
        Test path_row property
        """
        test_value = 'rtrquykdsacvshzstdbv'
        self.instance.path_row = test_value
        self.assertEqual(self.instance.path_row, test_value)
    
    def test_publish_month_property(self):
        """
        Test publish_month property
        """
        test_value = 'hlbprexeeihqcbfhdvbw'
        self.instance.publish_month = test_value
        self.assertEqual(self.instance.publish_month, test_value)
    
    def test_centroid_latitude_property(self):
        """
        Test centroid_latitude property
        """
        test_value = float(77.85751710385298)
        self.instance.centroid_latitude = test_value
        self.assertEqual(self.instance.centroid_latitude, test_value)
    
    def test_centroid_longitude_property(self):
        """
        Test centroid_longitude property
        """
        test_value = float(67.01249009092516)
        self.instance.centroid_longitude = test_value
        self.assertEqual(self.instance.centroid_longitude, test_value)
    
    def test_state_slug_property(self):
        """
        Test state_slug property
        """
        test_value = 'xumrirtfmxaydgmppbvc'
        self.instance.state_slug = test_value
        self.assertEqual(self.instance.state_slug, test_value)
    
    def test_class_slug_property(self):
        """
        Test class_slug property
        """
        test_value = ClassSlugenum.desmatamento_MINUScr
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

