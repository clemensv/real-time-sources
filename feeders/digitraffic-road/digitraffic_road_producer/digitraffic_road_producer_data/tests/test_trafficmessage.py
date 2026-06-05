"""
Test case for TrafficMessage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_road_producer_data.trafficmessage import TrafficMessage


class Test_TrafficMessage(unittest.TestCase):
    """
    Test case for TrafficMessage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TrafficMessage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TrafficMessage for testing
        """
        instance = TrafficMessage(
            situation_id='czuzjnpdjhdffadkxxlp',
            situation_type='oujtewtpyajxrsfdeccg',
            traffic_announcement_type='fddfskjzpqjscglsvomp',
            version=int(58),
            release_time='uygoqigcqpcnaeclkanz',
            version_time='xaxbworfyiwlvojmvatv',
            title='jaktdaulddrjkjjtoqkx',
            language='qsmfhdklcytkiodpulrl',
            sender='vgfcdrjapvrzfemmbljg',
            location_description='fyrlceinehwvazrdxnkt',
            start_time='anozujhzpvbzepxtkuyu',
            end_time='vmrrbgahedkanpadzlpe',
            features_json='kwkomegqhhwfpyziqvid',
            road_work_phases_json='gqjydmdzisjbtdeyffaz',
            comment='zytxjiycuvnjfbhfuycf',
            additional_information='qdjbevqnbunodslaohaf',
            contact_phone='undjrdbrsdfaujxzhcbb',
            contact_email='fjkgdscqvvnlxevnbqrs',
            announcements_json='mmofzjedwkrrftjswyre',
            geometry_type='emapbymqfbkqmjhunhjy',
            geometry_coordinates_json='wkgjmypxncvggxydmphg'
        )
        return instance

    
    def test_situation_id_property(self):
        """
        Test situation_id property
        """
        test_value = 'czuzjnpdjhdffadkxxlp'
        self.instance.situation_id = test_value
        self.assertEqual(self.instance.situation_id, test_value)
    
    def test_situation_type_property(self):
        """
        Test situation_type property
        """
        test_value = 'oujtewtpyajxrsfdeccg'
        self.instance.situation_type = test_value
        self.assertEqual(self.instance.situation_type, test_value)
    
    def test_traffic_announcement_type_property(self):
        """
        Test traffic_announcement_type property
        """
        test_value = 'fddfskjzpqjscglsvomp'
        self.instance.traffic_announcement_type = test_value
        self.assertEqual(self.instance.traffic_announcement_type, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = int(58)
        self.instance.version = test_value
        self.assertEqual(self.instance.version, test_value)
    
    def test_release_time_property(self):
        """
        Test release_time property
        """
        test_value = 'uygoqigcqpcnaeclkanz'
        self.instance.release_time = test_value
        self.assertEqual(self.instance.release_time, test_value)
    
    def test_version_time_property(self):
        """
        Test version_time property
        """
        test_value = 'xaxbworfyiwlvojmvatv'
        self.instance.version_time = test_value
        self.assertEqual(self.instance.version_time, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'jaktdaulddrjkjjtoqkx'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'qsmfhdklcytkiodpulrl'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_sender_property(self):
        """
        Test sender property
        """
        test_value = 'vgfcdrjapvrzfemmbljg'
        self.instance.sender = test_value
        self.assertEqual(self.instance.sender, test_value)
    
    def test_location_description_property(self):
        """
        Test location_description property
        """
        test_value = 'fyrlceinehwvazrdxnkt'
        self.instance.location_description = test_value
        self.assertEqual(self.instance.location_description, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'anozujhzpvbzepxtkuyu'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'vmrrbgahedkanpadzlpe'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_features_json_property(self):
        """
        Test features_json property
        """
        test_value = 'kwkomegqhhwfpyziqvid'
        self.instance.features_json = test_value
        self.assertEqual(self.instance.features_json, test_value)
    
    def test_road_work_phases_json_property(self):
        """
        Test road_work_phases_json property
        """
        test_value = 'gqjydmdzisjbtdeyffaz'
        self.instance.road_work_phases_json = test_value
        self.assertEqual(self.instance.road_work_phases_json, test_value)
    
    def test_comment_property(self):
        """
        Test comment property
        """
        test_value = 'zytxjiycuvnjfbhfuycf'
        self.instance.comment = test_value
        self.assertEqual(self.instance.comment, test_value)
    
    def test_additional_information_property(self):
        """
        Test additional_information property
        """
        test_value = 'qdjbevqnbunodslaohaf'
        self.instance.additional_information = test_value
        self.assertEqual(self.instance.additional_information, test_value)
    
    def test_contact_phone_property(self):
        """
        Test contact_phone property
        """
        test_value = 'undjrdbrsdfaujxzhcbb'
        self.instance.contact_phone = test_value
        self.assertEqual(self.instance.contact_phone, test_value)
    
    def test_contact_email_property(self):
        """
        Test contact_email property
        """
        test_value = 'fjkgdscqvvnlxevnbqrs'
        self.instance.contact_email = test_value
        self.assertEqual(self.instance.contact_email, test_value)
    
    def test_announcements_json_property(self):
        """
        Test announcements_json property
        """
        test_value = 'mmofzjedwkrrftjswyre'
        self.instance.announcements_json = test_value
        self.assertEqual(self.instance.announcements_json, test_value)
    
    def test_geometry_type_property(self):
        """
        Test geometry_type property
        """
        test_value = 'emapbymqfbkqmjhunhjy'
        self.instance.geometry_type = test_value
        self.assertEqual(self.instance.geometry_type, test_value)
    
    def test_geometry_coordinates_json_property(self):
        """
        Test geometry_coordinates_json property
        """
        test_value = 'wkgjmypxncvggxydmphg'
        self.instance.geometry_coordinates_json = test_value
        self.assertEqual(self.instance.geometry_coordinates_json, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TrafficMessage.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TrafficMessage.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

