"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hubeau_hydrometrie_producer_data.observation import Observation
import datetime


class Test_Observation(unittest.TestCase):
    """
    Test case for Observation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Observation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Observation for testing
        """
        instance = Observation(
            code_station='ipqkzgdccnxusazbewqo',
            date_obs=datetime.datetime.now(datetime.timezone.utc),
            resultat_obs=float(97.50450241146117),
            grandeur_hydro='tshmjctncxcgqyiqrnlt',
            libelle_methode_obs='hpwtwdyaekmjmsfzmonc',
            libelle_qualification_obs='awcuzkpwsmdcmawxvoxj'
        )
        return instance

    
    def test_code_station_property(self):
        """
        Test code_station property
        """
        test_value = 'ipqkzgdccnxusazbewqo'
        self.instance.code_station = test_value
        self.assertEqual(self.instance.code_station, test_value)
    
    def test_date_obs_property(self):
        """
        Test date_obs property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.date_obs = test_value
        self.assertEqual(self.instance.date_obs, test_value)
    
    def test_resultat_obs_property(self):
        """
        Test resultat_obs property
        """
        test_value = float(97.50450241146117)
        self.instance.resultat_obs = test_value
        self.assertEqual(self.instance.resultat_obs, test_value)
    
    def test_grandeur_hydro_property(self):
        """
        Test grandeur_hydro property
        """
        test_value = 'tshmjctncxcgqyiqrnlt'
        self.instance.grandeur_hydro = test_value
        self.assertEqual(self.instance.grandeur_hydro, test_value)
    
    def test_libelle_methode_obs_property(self):
        """
        Test libelle_methode_obs property
        """
        test_value = 'hpwtwdyaekmjmsfzmonc'
        self.instance.libelle_methode_obs = test_value
        self.assertEqual(self.instance.libelle_methode_obs, test_value)
    
    def test_libelle_qualification_obs_property(self):
        """
        Test libelle_qualification_obs property
        """
        test_value = 'awcuzkpwsmdcmawxvoxj'
        self.instance.libelle_qualification_obs = test_value
        self.assertEqual(self.instance.libelle_qualification_obs, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Observation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Observation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

