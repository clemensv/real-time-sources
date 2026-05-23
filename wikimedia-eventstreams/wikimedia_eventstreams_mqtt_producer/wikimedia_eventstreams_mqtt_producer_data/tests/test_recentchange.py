"""
Test case for RecentChange
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wikimedia_eventstreams_mqtt_producer_data.recentchange import RecentChange
from wikimedia_eventstreams_mqtt_producer_data.unnamedclass import UnnamedClass


class Test_RecentChange(unittest.TestCase):
    """
    Test case for RecentChange
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RecentChange.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RecentChange for testing
        """
        instance = RecentChange(
            event_id='wrqqkzpojxiqbrzwyuir',
            event_time='chjiobduxyxkgzobxtce',
            schema_uri='nrynosdfgfgcsmigukyk',
            meta=None,
            id='sgtvrrhtufccnzmwuvvj',
            type='cynsgokriuwspjrcynsd',
            namespace=int(26),
            title='hzavklynlvhvybqavkll',
            title_url='hnklxcwaeaplvlfnlvxg',
            comment='xsbtbmqpefojwnkukyzc',
            timestamp=int(13),
            user='tlmhrsikxxegtwfhplxt',
            bot=True,
            minor=False,
            patrolled=True,
            length=None,
            revision=None,
            server_url='wdfmqkuujtyfsvhsyncu',
            server_name='vrdafjdecnypfucoegxw',
            server_script_path='wiwbzdxwjxzczepynbsb',
            wiki='imkanrxrkesukxyiijgl',
            namespace_bucket='qoxdcthkspfviqevlfme',
            parsedcomment='yxtqcrjuvgivazzjkusx',
            notify_url='wvxeavxqvttgyurgdgbd',
            log_type='mlzhtatidqlsrkfrzmnk',
            log_action='fiesktcjiatvzonbxxvx',
            log_action_comment='pmayxmyelzhchgabmpij',
            log_id='gzavyltbuozqccryxocn',
            log_params_json='fqbhbaguekvwsoapnsfa'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'wrqqkzpojxiqbrzwyuir'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_event_time_property(self):
        """
        Test event_time property
        """
        test_value = 'chjiobduxyxkgzobxtce'
        self.instance.event_time = test_value
        self.assertEqual(self.instance.event_time, test_value)
    
    def test_schema_uri_property(self):
        """
        Test schema_uri property
        """
        test_value = 'nrynosdfgfgcsmigukyk'
        self.instance.schema_uri = test_value
        self.assertEqual(self.instance.schema_uri, test_value)
    
    def test_meta_property(self):
        """
        Test meta property
        """
        test_value = None
        self.instance.meta = test_value
        self.assertEqual(self.instance.meta, test_value)
    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'sgtvrrhtufccnzmwuvvj'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'cynsgokriuwspjrcynsd'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_namespace_property(self):
        """
        Test namespace property
        """
        test_value = int(26)
        self.instance.namespace = test_value
        self.assertEqual(self.instance.namespace, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'hzavklynlvhvybqavkll'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_title_url_property(self):
        """
        Test title_url property
        """
        test_value = 'hnklxcwaeaplvlfnlvxg'
        self.instance.title_url = test_value
        self.assertEqual(self.instance.title_url, test_value)
    
    def test_comment_property(self):
        """
        Test comment property
        """
        test_value = 'xsbtbmqpefojwnkukyzc'
        self.instance.comment = test_value
        self.assertEqual(self.instance.comment, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = int(13)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_user_property(self):
        """
        Test user property
        """
        test_value = 'tlmhrsikxxegtwfhplxt'
        self.instance.user = test_value
        self.assertEqual(self.instance.user, test_value)
    
    def test_bot_property(self):
        """
        Test bot property
        """
        test_value = True
        self.instance.bot = test_value
        self.assertEqual(self.instance.bot, test_value)
    
    def test_minor_property(self):
        """
        Test minor property
        """
        test_value = False
        self.instance.minor = test_value
        self.assertEqual(self.instance.minor, test_value)
    
    def test_patrolled_property(self):
        """
        Test patrolled property
        """
        test_value = True
        self.instance.patrolled = test_value
        self.assertEqual(self.instance.patrolled, test_value)
    
    def test_length_property(self):
        """
        Test length property
        """
        test_value = None
        self.instance.length = test_value
        self.assertEqual(self.instance.length, test_value)
    
    def test_revision_property(self):
        """
        Test revision property
        """
        test_value = None
        self.instance.revision = test_value
        self.assertEqual(self.instance.revision, test_value)
    
    def test_server_url_property(self):
        """
        Test server_url property
        """
        test_value = 'wdfmqkuujtyfsvhsyncu'
        self.instance.server_url = test_value
        self.assertEqual(self.instance.server_url, test_value)
    
    def test_server_name_property(self):
        """
        Test server_name property
        """
        test_value = 'vrdafjdecnypfucoegxw'
        self.instance.server_name = test_value
        self.assertEqual(self.instance.server_name, test_value)
    
    def test_server_script_path_property(self):
        """
        Test server_script_path property
        """
        test_value = 'wiwbzdxwjxzczepynbsb'
        self.instance.server_script_path = test_value
        self.assertEqual(self.instance.server_script_path, test_value)
    
    def test_wiki_property(self):
        """
        Test wiki property
        """
        test_value = 'imkanrxrkesukxyiijgl'
        self.instance.wiki = test_value
        self.assertEqual(self.instance.wiki, test_value)
    
    def test_namespace_bucket_property(self):
        """
        Test namespace_bucket property
        """
        test_value = 'qoxdcthkspfviqevlfme'
        self.instance.namespace_bucket = test_value
        self.assertEqual(self.instance.namespace_bucket, test_value)
    
    def test_parsedcomment_property(self):
        """
        Test parsedcomment property
        """
        test_value = 'yxtqcrjuvgivazzjkusx'
        self.instance.parsedcomment = test_value
        self.assertEqual(self.instance.parsedcomment, test_value)
    
    def test_notify_url_property(self):
        """
        Test notify_url property
        """
        test_value = 'wvxeavxqvttgyurgdgbd'
        self.instance.notify_url = test_value
        self.assertEqual(self.instance.notify_url, test_value)
    
    def test_log_type_property(self):
        """
        Test log_type property
        """
        test_value = 'mlzhtatidqlsrkfrzmnk'
        self.instance.log_type = test_value
        self.assertEqual(self.instance.log_type, test_value)
    
    def test_log_action_property(self):
        """
        Test log_action property
        """
        test_value = 'fiesktcjiatvzonbxxvx'
        self.instance.log_action = test_value
        self.assertEqual(self.instance.log_action, test_value)
    
    def test_log_action_comment_property(self):
        """
        Test log_action_comment property
        """
        test_value = 'pmayxmyelzhchgabmpij'
        self.instance.log_action_comment = test_value
        self.assertEqual(self.instance.log_action_comment, test_value)
    
    def test_log_id_property(self):
        """
        Test log_id property
        """
        test_value = 'gzavyltbuozqccryxocn'
        self.instance.log_id = test_value
        self.assertEqual(self.instance.log_id, test_value)
    
    def test_log_params_json_property(self):
        """
        Test log_params_json property
        """
        test_value = 'fqbhbaguekvwsoapnsfa'
        self.instance.log_params_json = test_value
        self.assertEqual(self.instance.log_params_json, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RecentChange.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RecentChange.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

