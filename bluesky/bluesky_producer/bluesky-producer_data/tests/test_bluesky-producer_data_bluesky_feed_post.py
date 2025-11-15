"""
Test case for Post
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bluesky-producer_data.bluesky.feed.post import Post


class Test_Post(unittest.TestCase):
    """
    Test case for Post
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Post.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Post for testing
        """
        instance = Post(
            uri='jkekrmmcttluteeejldb',
            cid='lcqxjfvzwmrndwpmrlhb',
            did='qljfeyvhxftrssxgeglk',
            handle='yjnfxiiytgmwforakqyl',
            text='uduhzxllqsyzspvsfswg',
            langs=['fsmlugwnatpjforjknlz', 'hhixjekcpfwlrpvkfajk', 'byyftbndpjsijrnfhmmh', 'qvlbsfsddianzzsetoxo', 'rzcgdubqifbfasnlxagk'],
            reply_parent='nysqjewphpjchqwbjohv',
            reply_root='gjmscoxpakxhvvluewvv',
            embed_type='vvtjxrfdyzoettcviugo',
            embed_uri='ywhivofubacbqkoickqa',
            facets='yogehbunrzrmknopjcyn',
            tags=['duqomuxrehpxyjlofpzt', 'yblvtvhyqaghbserldqf', 'xdkvfrkduxpdcwjspqki', 'fiqdrlehzlgwpvmtxwkw'],
            created_at='yfkniatnxhomnfuvfapo',
            indexed_at='tiacpawbdfazhersopdw',
            seq=int(40)
        )
        return instance

    
    def test_uri_property(self):
        """
        Test uri property
        """
        test_value = 'jkekrmmcttluteeejldb'
        self.instance.uri = test_value
        self.assertEqual(self.instance.uri, test_value)
    
    def test_cid_property(self):
        """
        Test cid property
        """
        test_value = 'lcqxjfvzwmrndwpmrlhb'
        self.instance.cid = test_value
        self.assertEqual(self.instance.cid, test_value)
    
    def test_did_property(self):
        """
        Test did property
        """
        test_value = 'qljfeyvhxftrssxgeglk'
        self.instance.did = test_value
        self.assertEqual(self.instance.did, test_value)
    
    def test_handle_property(self):
        """
        Test handle property
        """
        test_value = 'yjnfxiiytgmwforakqyl'
        self.instance.handle = test_value
        self.assertEqual(self.instance.handle, test_value)
    
    def test_text_property(self):
        """
        Test text property
        """
        test_value = 'uduhzxllqsyzspvsfswg'
        self.instance.text = test_value
        self.assertEqual(self.instance.text, test_value)
    
    def test_langs_property(self):
        """
        Test langs property
        """
        test_value = ['fsmlugwnatpjforjknlz', 'hhixjekcpfwlrpvkfajk', 'byyftbndpjsijrnfhmmh', 'qvlbsfsddianzzsetoxo', 'rzcgdubqifbfasnlxagk']
        self.instance.langs = test_value
        self.assertEqual(self.instance.langs, test_value)
    
    def test_reply_parent_property(self):
        """
        Test reply_parent property
        """
        test_value = 'nysqjewphpjchqwbjohv'
        self.instance.reply_parent = test_value
        self.assertEqual(self.instance.reply_parent, test_value)
    
    def test_reply_root_property(self):
        """
        Test reply_root property
        """
        test_value = 'gjmscoxpakxhvvluewvv'
        self.instance.reply_root = test_value
        self.assertEqual(self.instance.reply_root, test_value)
    
    def test_embed_type_property(self):
        """
        Test embed_type property
        """
        test_value = 'vvtjxrfdyzoettcviugo'
        self.instance.embed_type = test_value
        self.assertEqual(self.instance.embed_type, test_value)
    
    def test_embed_uri_property(self):
        """
        Test embed_uri property
        """
        test_value = 'ywhivofubacbqkoickqa'
        self.instance.embed_uri = test_value
        self.assertEqual(self.instance.embed_uri, test_value)
    
    def test_facets_property(self):
        """
        Test facets property
        """
        test_value = 'yogehbunrzrmknopjcyn'
        self.instance.facets = test_value
        self.assertEqual(self.instance.facets, test_value)
    
    def test_tags_property(self):
        """
        Test tags property
        """
        test_value = ['duqomuxrehpxyjlofpzt', 'yblvtvhyqaghbserldqf', 'xdkvfrkduxpdcwjspqki', 'fiqdrlehzlgwpvmtxwkw']
        self.instance.tags = test_value
        self.assertEqual(self.instance.tags, test_value)
    
    def test_created_at_property(self):
        """
        Test created_at property
        """
        test_value = 'yfkniatnxhomnfuvfapo'
        self.instance.created_at = test_value
        self.assertEqual(self.instance.created_at, test_value)
    
    def test_indexed_at_property(self):
        """
        Test indexed_at property
        """
        test_value = 'tiacpawbdfazhersopdw'
        self.instance.indexed_at = test_value
        self.assertEqual(self.instance.indexed_at, test_value)
    
    def test_seq_property(self):
        """
        Test seq property
        """
        test_value = int(40)
        self.instance.seq = test_value
        self.assertEqual(self.instance.seq, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Post.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
