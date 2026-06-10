"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hubeau_hydrometrie_amqp_producer_data.station import Station


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
            code_station='ydidiothknwkdrhsekuj',
            libelle_station='ttfdekpvzragslrlovxw',
            code_site='wgutzvtcfrhqfsksaxfl',
            longitude_station=float(82.27219456001006),
            latitude_station=float(92.44534096998315),
            libelle_cours_eau='tsnbmvscvujjcaixdkax',
            libelle_commune='mpmfyncijgzwoocbdpdz',
            code_departement='yzzrgbisccicyljruuow',
            en_service=False,
            date_ouverture_station='adxeprzqlmwnxnfnijgd',
            basin='niyeclrsxuwhoffbijsl'
        )
        return instance

    
    def test_code_station_property(self):
        """
        Test code_station property
        """
        test_value = 'ydidiothknwkdrhsekuj'
        self.instance.code_station = test_value
        self.assertEqual(self.instance.code_station, test_value)
    
    def test_libelle_station_property(self):
        """
        Test libelle_station property
        """
        test_value = 'ttfdekpvzragslrlovxw'
        self.instance.libelle_station = test_value
        self.assertEqual(self.instance.libelle_station, test_value)
    
    def test_code_site_property(self):
        """
        Test code_site property
        """
        test_value = 'wgutzvtcfrhqfsksaxfl'
        self.instance.code_site = test_value
        self.assertEqual(self.instance.code_site, test_value)
    
    def test_longitude_station_property(self):
        """
        Test longitude_station property
        """
        test_value = float(82.27219456001006)
        self.instance.longitude_station = test_value
        self.assertEqual(self.instance.longitude_station, test_value)
    
    def test_latitude_station_property(self):
        """
        Test latitude_station property
        """
        test_value = float(92.44534096998315)
        self.instance.latitude_station = test_value
        self.assertEqual(self.instance.latitude_station, test_value)
    
    def test_libelle_cours_eau_property(self):
        """
        Test libelle_cours_eau property
        """
        test_value = 'tsnbmvscvujjcaixdkax'
        self.instance.libelle_cours_eau = test_value
        self.assertEqual(self.instance.libelle_cours_eau, test_value)
    
    def test_libelle_commune_property(self):
        """
        Test libelle_commune property
        """
        test_value = 'mpmfyncijgzwoocbdpdz'
        self.instance.libelle_commune = test_value
        self.assertEqual(self.instance.libelle_commune, test_value)
    
    def test_code_departement_property(self):
        """
        Test code_departement property
        """
        test_value = 'yzzrgbisccicyljruuow'
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
        test_value = 'adxeprzqlmwnxnfnijgd'
        self.instance.date_ouverture_station = test_value
        self.assertEqual(self.instance.date_ouverture_station, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'niyeclrsxuwhoffbijsl'
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

