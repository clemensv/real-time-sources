"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hubeau_hydrometrie_producer_data.fr.gov.eaufrance.hubeau.hydrometrie.station import Station


class Test_Station(unittest.TestCase):
    """
    Test case for Station
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station for testing
        """
        instance = Station(
            code_station='ruhrximkgasalmbyuzti',
            libelle_station='zzmilfijcbgbuvsvrkkv',
            code_site='khugreqrnwvpvelazgvl',
            longitude_station=float(17.441023918870435),
            latitude_station=float(49.85003404956076),
            libelle_cours_eau='kkoymnfsvtbkkjocmdus',
            libelle_commune='zzankurififqmoesdwgn',
            code_departement='ubegrwaskacbwxfbmloj',
            en_service=True,
            date_ouverture_station='alqcsklxlbvfaezfrepp'
        )
        return instance

    
    def test_code_station_property(self):
        """
        Test code_station property
        """
        test_value = 'ruhrximkgasalmbyuzti'
        self.instance.code_station = test_value
        self.assertEqual(self.instance.code_station, test_value)
    
    def test_libelle_station_property(self):
        """
        Test libelle_station property
        """
        test_value = 'zzmilfijcbgbuvsvrkkv'
        self.instance.libelle_station = test_value
        self.assertEqual(self.instance.libelle_station, test_value)
    
    def test_code_site_property(self):
        """
        Test code_site property
        """
        test_value = 'khugreqrnwvpvelazgvl'
        self.instance.code_site = test_value
        self.assertEqual(self.instance.code_site, test_value)
    
    def test_longitude_station_property(self):
        """
        Test longitude_station property
        """
        test_value = float(17.441023918870435)
        self.instance.longitude_station = test_value
        self.assertEqual(self.instance.longitude_station, test_value)
    
    def test_latitude_station_property(self):
        """
        Test latitude_station property
        """
        test_value = float(49.85003404956076)
        self.instance.latitude_station = test_value
        self.assertEqual(self.instance.latitude_station, test_value)
    
    def test_libelle_cours_eau_property(self):
        """
        Test libelle_cours_eau property
        """
        test_value = 'kkoymnfsvtbkkjocmdus'
        self.instance.libelle_cours_eau = test_value
        self.assertEqual(self.instance.libelle_cours_eau, test_value)
    
    def test_libelle_commune_property(self):
        """
        Test libelle_commune property
        """
        test_value = 'zzankurififqmoesdwgn'
        self.instance.libelle_commune = test_value
        self.assertEqual(self.instance.libelle_commune, test_value)
    
    def test_code_departement_property(self):
        """
        Test code_departement property
        """
        test_value = 'ubegrwaskacbwxfbmloj'
        self.instance.code_departement = test_value
        self.assertEqual(self.instance.code_departement, test_value)
    
    def test_en_service_property(self):
        """
        Test en_service property
        """
        test_value = True
        self.instance.en_service = test_value
        self.assertEqual(self.instance.en_service, test_value)
    
    def test_date_ouverture_station_property(self):
        """
        Test date_ouverture_station property
        """
        test_value = 'alqcsklxlbvfaezfrepp'
        self.instance.date_ouverture_station = test_value
        self.assertEqual(self.instance.date_ouverture_station, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
