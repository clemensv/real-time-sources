"""
Test case for Agency
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_mqtt_producer_data.generaltransitfeedstatic.agency import Agency


class Test_Agency(unittest.TestCase):
    """
    Test case for Agency
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Agency.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Agency for testing
        """
        instance = Agency(
            agencyId='iirbwonnljuohjvgiutk',
            agencyName='cdajanutoprzkvwmxnzb',
            agencyUrl='phihrsfvlznvvvhkpthp',
            agencyTimezone='jqksqfbarbldjlfurtjg',
            agencyLang='jnjrjkerxqvzfhemczqi',
            agencyPhone='rhjnqlnfrhegrmfuagfr',
            agencyFareUrl='arellycdtyokvepzdleb',
            agencyEmail='iaxderkffzdhynddxlfv'
        )
        return instance

    
    def test_agencyId_property(self):
        """
        Test agencyId property
        """
        test_value = 'iirbwonnljuohjvgiutk'
        self.instance.agencyId = test_value
        self.assertEqual(self.instance.agencyId, test_value)
    
    def test_agencyName_property(self):
        """
        Test agencyName property
        """
        test_value = 'cdajanutoprzkvwmxnzb'
        self.instance.agencyName = test_value
        self.assertEqual(self.instance.agencyName, test_value)
    
    def test_agencyUrl_property(self):
        """
        Test agencyUrl property
        """
        test_value = 'phihrsfvlznvvvhkpthp'
        self.instance.agencyUrl = test_value
        self.assertEqual(self.instance.agencyUrl, test_value)
    
    def test_agencyTimezone_property(self):
        """
        Test agencyTimezone property
        """
        test_value = 'jqksqfbarbldjlfurtjg'
        self.instance.agencyTimezone = test_value
        self.assertEqual(self.instance.agencyTimezone, test_value)
    
    def test_agencyLang_property(self):
        """
        Test agencyLang property
        """
        test_value = 'jnjrjkerxqvzfhemczqi'
        self.instance.agencyLang = test_value
        self.assertEqual(self.instance.agencyLang, test_value)
    
    def test_agencyPhone_property(self):
        """
        Test agencyPhone property
        """
        test_value = 'rhjnqlnfrhegrmfuagfr'
        self.instance.agencyPhone = test_value
        self.assertEqual(self.instance.agencyPhone, test_value)
    
    def test_agencyFareUrl_property(self):
        """
        Test agencyFareUrl property
        """
        test_value = 'arellycdtyokvepzdleb'
        self.instance.agencyFareUrl = test_value
        self.assertEqual(self.instance.agencyFareUrl, test_value)
    
    def test_agencyEmail_property(self):
        """
        Test agencyEmail property
        """
        test_value = 'iaxderkffzdhynddxlfv'
        self.instance.agencyEmail = test_value
        self.assertEqual(self.instance.agencyEmail, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Agency.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Agency.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

