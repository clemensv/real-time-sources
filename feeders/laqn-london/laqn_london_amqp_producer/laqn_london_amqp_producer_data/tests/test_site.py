"""
Test case for Site
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from laqn_london_amqp_producer_data.uk.kcl.laqn.site import Site
from laqn_london_amqp_producer_data.uk.kcl.laqn.sitetypeenum import SiteTypeenum


class Test_Site(unittest.TestCase):
    """
    Test case for Site
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Site.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Site for testing
        """
        instance = Site(
            site_code='drnosagpisafqqiykrms',
            site_name='xtrtfwxqtgispswumngb',
            site_type=SiteTypeenum.Suburban,
            local_authority_code='frtiuaekectmsxjozxwo',
            local_authority_name='hlqoyktyporhvzzvfqsg',
            latitude=float(78.27156911716851),
            longitude=float(12.910025081118038),
            date_opened='omwvlhzplkoieuihzwpb',
            date_closed='tydiahtarfkzcwrcskwb',
            data_owner='aradesszjftgimucubbe',
            data_manager='sjznunxkwytedotoeddw'
        )
        return instance

    
    def test_site_code_property(self):
        """
        Test site_code property
        """
        test_value = 'drnosagpisafqqiykrms'
        self.instance.site_code = test_value
        self.assertEqual(self.instance.site_code, test_value)
    
    def test_site_name_property(self):
        """
        Test site_name property
        """
        test_value = 'xtrtfwxqtgispswumngb'
        self.instance.site_name = test_value
        self.assertEqual(self.instance.site_name, test_value)
    
    def test_site_type_property(self):
        """
        Test site_type property
        """
        test_value = SiteTypeenum.Suburban
        self.instance.site_type = test_value
        self.assertEqual(self.instance.site_type, test_value)
    
    def test_local_authority_code_property(self):
        """
        Test local_authority_code property
        """
        test_value = 'frtiuaekectmsxjozxwo'
        self.instance.local_authority_code = test_value
        self.assertEqual(self.instance.local_authority_code, test_value)
    
    def test_local_authority_name_property(self):
        """
        Test local_authority_name property
        """
        test_value = 'hlqoyktyporhvzzvfqsg'
        self.instance.local_authority_name = test_value
        self.assertEqual(self.instance.local_authority_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(78.27156911716851)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(12.910025081118038)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_date_opened_property(self):
        """
        Test date_opened property
        """
        test_value = 'omwvlhzplkoieuihzwpb'
        self.instance.date_opened = test_value
        self.assertEqual(self.instance.date_opened, test_value)
    
    def test_date_closed_property(self):
        """
        Test date_closed property
        """
        test_value = 'tydiahtarfkzcwrcskwb'
        self.instance.date_closed = test_value
        self.assertEqual(self.instance.date_closed, test_value)
    
    def test_data_owner_property(self):
        """
        Test data_owner property
        """
        test_value = 'aradesszjftgimucubbe'
        self.instance.data_owner = test_value
        self.assertEqual(self.instance.data_owner, test_value)
    
    def test_data_manager_property(self):
        """
        Test data_manager property
        """
        test_value = 'sjznunxkwytedotoeddw'
        self.instance.data_manager = test_value
        self.assertEqual(self.instance.data_manager, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Site.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Site.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

