"""
Test case for FareMedia
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.faremedia import FareMedia


class Test_FareMedia(unittest.TestCase):
    """
    Test case for FareMedia
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FareMedia.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FareMedia for testing
        """
        instance = FareMedia(
            fareMediaId='mkgpwmldkorktgrprpwu',
            fareMediaName='uyjtooxnhmhymlzrxcsp',
            fareMediaDesc='gexwttappsphvmnptzga',
            fareMediaUrl='jfnsddgdxwaboedkypny'
        )
        return instance

    
    def test_fareMediaId_property(self):
        """
        Test fareMediaId property
        """
        test_value = 'mkgpwmldkorktgrprpwu'
        self.instance.fareMediaId = test_value
        self.assertEqual(self.instance.fareMediaId, test_value)
    
    def test_fareMediaName_property(self):
        """
        Test fareMediaName property
        """
        test_value = 'uyjtooxnhmhymlzrxcsp'
        self.instance.fareMediaName = test_value
        self.assertEqual(self.instance.fareMediaName, test_value)
    
    def test_fareMediaDesc_property(self):
        """
        Test fareMediaDesc property
        """
        test_value = 'gexwttappsphvmnptzga'
        self.instance.fareMediaDesc = test_value
        self.assertEqual(self.instance.fareMediaDesc, test_value)
    
    def test_fareMediaUrl_property(self):
        """
        Test fareMediaUrl property
        """
        test_value = 'jfnsddgdxwaboedkypny'
        self.instance.fareMediaUrl = test_value
        self.assertEqual(self.instance.fareMediaUrl, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FareMedia.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
