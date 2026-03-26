"""
Test case for Record
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hubeau_hydrometrie_producer_data.record import Record


class Test_Record(unittest.TestCase):
    """
    Test case for Record
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Record.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Record for testing
        """
        instance = Record(
            code_station='amuvqioannazjephrxtj',
            libelle_station='vtpppldnxknnspvkxbdl',
            code_site='twcesasjtinppnexbqvq',
            longitude_station=float(98.16029686799584),
            latitude_station=float(47.62419004659143),
            libelle_cours_eau='chzelmezkeylwodjrust',
            libelle_commune='zaekudwnjlucjoynsydj',
            code_departement='lnxptonioatljjsurdbf',
            en_service=False,
            date_ouverture_station='pypvykpolbianmphwevk'
        )
        return instance

    
    def test_code_station_property(self):
        """
        Test code_station property
        """
        test_value = 'amuvqioannazjephrxtj'
        self.instance.code_station = test_value
        self.assertEqual(self.instance.code_station, test_value)
    
    def test_libelle_station_property(self):
        """
        Test libelle_station property
        """
        test_value = 'vtpppldnxknnspvkxbdl'
        self.instance.libelle_station = test_value
        self.assertEqual(self.instance.libelle_station, test_value)
    
    def test_code_site_property(self):
        """
        Test code_site property
        """
        test_value = 'twcesasjtinppnexbqvq'
        self.instance.code_site = test_value
        self.assertEqual(self.instance.code_site, test_value)
    
    def test_longitude_station_property(self):
        """
        Test longitude_station property
        """
        test_value = float(98.16029686799584)
        self.instance.longitude_station = test_value
        self.assertEqual(self.instance.longitude_station, test_value)
    
    def test_latitude_station_property(self):
        """
        Test latitude_station property
        """
        test_value = float(47.62419004659143)
        self.instance.latitude_station = test_value
        self.assertEqual(self.instance.latitude_station, test_value)
    
    def test_libelle_cours_eau_property(self):
        """
        Test libelle_cours_eau property
        """
        test_value = 'chzelmezkeylwodjrust'
        self.instance.libelle_cours_eau = test_value
        self.assertEqual(self.instance.libelle_cours_eau, test_value)
    
    def test_libelle_commune_property(self):
        """
        Test libelle_commune property
        """
        test_value = 'zaekudwnjlucjoynsydj'
        self.instance.libelle_commune = test_value
        self.assertEqual(self.instance.libelle_commune, test_value)
    
    def test_code_departement_property(self):
        """
        Test code_departement property
        """
        test_value = 'lnxptonioatljjsurdbf'
        self.instance.code_departement = test_value
        self.assertEqual(self.instance.code_departement, test_value)
    
    def test_en_service_property(self):
        """
        Test en_service property
        """
        test_value = False
        self.instance.en_service = test_value
        self.assertEqual(self.instance.en_service, test_value)
    
    def test_date_ouverture_station_property(self):
        """
        Test date_ouverture_station property
        """
        test_value = 'pypvykpolbianmphwevk'
        self.instance.date_ouverture_station = test_value
        self.assertEqual(self.instance.date_ouverture_station, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Record.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
