"""
Test case for Post
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bluesky_producer_data.bluesky.feed.post import Post


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
            uri='gkhrbgqeqfuvhtluvuzm',
            cid='fdupmgalxcbcptjkcqlb',
            did='ezffbjacladjcozexgxa',
            handle='gzszonsmmwhyqqxxqjii',
            text='akbndyotcxtjjkubqvse',
            langs=['mhlgloeynkoixbcdapuj', 'svcggvldpuprsyzacvxz', 'huzztevxjzblrvhvvian', 'uthydnwncxudwduilwoa', 'rgqakocakxvaqgimkfgy'],
            reply_parent='njskcczviamsarqqpcxh',
            reply_root='jqszvszebukkvdfgphkw',
            embed_type='sdfpyrwgwyqnkmtgtejf',
            embed_uri='ezcsjiyqwlvaxikoldog',
            facets='qjnwfryzbbhynzysneqe',
            tags=['gmobcdrsjwvezovoqzjo'],
            created_at='yoatwzhjlqqadqcdfurp',
            indexed_at='hsnxiqdcopjlstbwvzbu',
            seq=int(20),
            collection='uwyrouxbwxjlleesppob',
            lang='pzkadfohzzuihmbtxmrw'
        )
        return instance

    
    def test_uri_property(self):
        """
        Test uri property
        """
        test_value = 'gkhrbgqeqfuvhtluvuzm'
        self.instance.uri = test_value
        self.assertEqual(self.instance.uri, test_value)
    
    def test_cid_property(self):
        """
        Test cid property
        """
        test_value = 'fdupmgalxcbcptjkcqlb'
        self.instance.cid = test_value
        self.assertEqual(self.instance.cid, test_value)
    
    def test_did_property(self):
        """
        Test did property
        """
        test_value = 'ezffbjacladjcozexgxa'
        self.instance.did = test_value
        self.assertEqual(self.instance.did, test_value)
    
    def test_handle_property(self):
        """
        Test handle property
        """
        test_value = 'gzszonsmmwhyqqxxqjii'
        self.instance.handle = test_value
        self.assertEqual(self.instance.handle, test_value)
    
    def test_text_property(self):
        """
        Test text property
        """
        test_value = 'akbndyotcxtjjkubqvse'
        self.instance.text = test_value
        self.assertEqual(self.instance.text, test_value)
    
    def test_langs_property(self):
        """
        Test langs property
        """
        test_value = ['mhlgloeynkoixbcdapuj', 'svcggvldpuprsyzacvxz', 'huzztevxjzblrvhvvian', 'uthydnwncxudwduilwoa', 'rgqakocakxvaqgimkfgy']
        self.instance.langs = test_value
        self.assertEqual(self.instance.langs, test_value)
    
    def test_reply_parent_property(self):
        """
        Test reply_parent property
        """
        test_value = 'njskcczviamsarqqpcxh'
        self.instance.reply_parent = test_value
        self.assertEqual(self.instance.reply_parent, test_value)
    
    def test_reply_root_property(self):
        """
        Test reply_root property
        """
        test_value = 'jqszvszebukkvdfgphkw'
        self.instance.reply_root = test_value
        self.assertEqual(self.instance.reply_root, test_value)
    
    def test_embed_type_property(self):
        """
        Test embed_type property
        """
        test_value = 'sdfpyrwgwyqnkmtgtejf'
        self.instance.embed_type = test_value
        self.assertEqual(self.instance.embed_type, test_value)
    
    def test_embed_uri_property(self):
        """
        Test embed_uri property
        """
        test_value = 'ezcsjiyqwlvaxikoldog'
        self.instance.embed_uri = test_value
        self.assertEqual(self.instance.embed_uri, test_value)
    
    def test_facets_property(self):
        """
        Test facets property
        """
        test_value = 'qjnwfryzbbhynzysneqe'
        self.instance.facets = test_value
        self.assertEqual(self.instance.facets, test_value)
    
    def test_tags_property(self):
        """
        Test tags property
        """
        test_value = ['gmobcdrsjwvezovoqzjo']
        self.instance.tags = test_value
        self.assertEqual(self.instance.tags, test_value)
    
    def test_created_at_property(self):
        """
        Test created_at property
        """
        test_value = 'yoatwzhjlqqadqcdfurp'
        self.instance.created_at = test_value
        self.assertEqual(self.instance.created_at, test_value)
    
    def test_indexed_at_property(self):
        """
        Test indexed_at property
        """
        test_value = 'hsnxiqdcopjlstbwvzbu'
        self.instance.indexed_at = test_value
        self.assertEqual(self.instance.indexed_at, test_value)
    
    def test_seq_property(self):
        """
        Test seq property
        """
        test_value = int(20)
        self.instance.seq = test_value
        self.assertEqual(self.instance.seq, test_value)
    
    def test_collection_property(self):
        """
        Test collection property
        """
        test_value = 'uwyrouxbwxjlleesppob'
        self.instance.collection = test_value
        self.assertEqual(self.instance.collection, test_value)
    
    def test_lang_property(self):
        """
        Test lang property
        """
        test_value = 'pzkadfohzzuihmbtxmrw'
        self.instance.lang = test_value
        self.assertEqual(self.instance.lang, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Post.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Post.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

