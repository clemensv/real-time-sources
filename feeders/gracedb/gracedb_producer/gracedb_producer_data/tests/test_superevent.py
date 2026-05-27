"""
Test case for Superevent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gracedb_producer_data.org.ligo.gracedb.superevent import Superevent


class Test_Superevent(unittest.TestCase):
    """
    Test case for Superevent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Superevent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Superevent for testing
        """
        instance = Superevent(
            superevent_id='vgswadfmfpgvmqujoujp',
            category='zzmobrbgiehfwstpshre',
            created='yzfntnforedezovacbct',
            t_start=float(32.58771595434175),
            t_0=float(85.28898271754592),
            t_end=float(74.10501221500893),
            far=float(66.04346105495111),
            time_coinc_far=float(41.047733283164256),
            space_coinc_far=float(54.06233743776223),
            labels_json='qmeudppyaiabcgpsfkld',
            preferred_event_id='qcjqhfzipfolorasxlrt',
            pipeline='isqnidjjcrduspqqiyrl',
            group='yefjkngjndmgdhexnpvm',
            instruments='rjlqmpckogpxkrdziexc',
            gw_id='aysvmshhglqjlbuekvvu',
            submitter='ptodddzaytcobsdymniw',
            em_type='hoefgetakotirsouexmd',
            search='edtfhkzkbhwhnvjujkyi',
            far_is_upper_limit=True,
            nevents=int(15),
            self_uri='iklmcskwezpypulptrcr'
        )
        return instance

    
    def test_superevent_id_property(self):
        """
        Test superevent_id property
        """
        test_value = 'vgswadfmfpgvmqujoujp'
        self.instance.superevent_id = test_value
        self.assertEqual(self.instance.superevent_id, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = 'zzmobrbgiehfwstpshre'
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_created_property(self):
        """
        Test created property
        """
        test_value = 'yzfntnforedezovacbct'
        self.instance.created = test_value
        self.assertEqual(self.instance.created, test_value)
    
    def test_t_start_property(self):
        """
        Test t_start property
        """
        test_value = float(32.58771595434175)
        self.instance.t_start = test_value
        self.assertEqual(self.instance.t_start, test_value)
    
    def test_t_0_property(self):
        """
        Test t_0 property
        """
        test_value = float(85.28898271754592)
        self.instance.t_0 = test_value
        self.assertEqual(self.instance.t_0, test_value)
    
    def test_t_end_property(self):
        """
        Test t_end property
        """
        test_value = float(74.10501221500893)
        self.instance.t_end = test_value
        self.assertEqual(self.instance.t_end, test_value)
    
    def test_far_property(self):
        """
        Test far property
        """
        test_value = float(66.04346105495111)
        self.instance.far = test_value
        self.assertEqual(self.instance.far, test_value)
    
    def test_time_coinc_far_property(self):
        """
        Test time_coinc_far property
        """
        test_value = float(41.047733283164256)
        self.instance.time_coinc_far = test_value
        self.assertEqual(self.instance.time_coinc_far, test_value)
    
    def test_space_coinc_far_property(self):
        """
        Test space_coinc_far property
        """
        test_value = float(54.06233743776223)
        self.instance.space_coinc_far = test_value
        self.assertEqual(self.instance.space_coinc_far, test_value)
    
    def test_labels_json_property(self):
        """
        Test labels_json property
        """
        test_value = 'qmeudppyaiabcgpsfkld'
        self.instance.labels_json = test_value
        self.assertEqual(self.instance.labels_json, test_value)
    
    def test_preferred_event_id_property(self):
        """
        Test preferred_event_id property
        """
        test_value = 'qcjqhfzipfolorasxlrt'
        self.instance.preferred_event_id = test_value
        self.assertEqual(self.instance.preferred_event_id, test_value)
    
    def test_pipeline_property(self):
        """
        Test pipeline property
        """
        test_value = 'isqnidjjcrduspqqiyrl'
        self.instance.pipeline = test_value
        self.assertEqual(self.instance.pipeline, test_value)
    
    def test_group_property(self):
        """
        Test group property
        """
        test_value = 'yefjkngjndmgdhexnpvm'
        self.instance.group = test_value
        self.assertEqual(self.instance.group, test_value)
    
    def test_instruments_property(self):
        """
        Test instruments property
        """
        test_value = 'rjlqmpckogpxkrdziexc'
        self.instance.instruments = test_value
        self.assertEqual(self.instance.instruments, test_value)
    
    def test_gw_id_property(self):
        """
        Test gw_id property
        """
        test_value = 'aysvmshhglqjlbuekvvu'
        self.instance.gw_id = test_value
        self.assertEqual(self.instance.gw_id, test_value)
    
    def test_submitter_property(self):
        """
        Test submitter property
        """
        test_value = 'ptodddzaytcobsdymniw'
        self.instance.submitter = test_value
        self.assertEqual(self.instance.submitter, test_value)
    
    def test_em_type_property(self):
        """
        Test em_type property
        """
        test_value = 'hoefgetakotirsouexmd'
        self.instance.em_type = test_value
        self.assertEqual(self.instance.em_type, test_value)
    
    def test_search_property(self):
        """
        Test search property
        """
        test_value = 'edtfhkzkbhwhnvjujkyi'
        self.instance.search = test_value
        self.assertEqual(self.instance.search, test_value)
    
    def test_far_is_upper_limit_property(self):
        """
        Test far_is_upper_limit property
        """
        test_value = True
        self.instance.far_is_upper_limit = test_value
        self.assertEqual(self.instance.far_is_upper_limit, test_value)
    
    def test_nevents_property(self):
        """
        Test nevents property
        """
        test_value = int(15)
        self.instance.nevents = test_value
        self.assertEqual(self.instance.nevents, test_value)
    
    def test_self_uri_property(self):
        """
        Test self_uri property
        """
        test_value = 'iklmcskwezpypulptrcr'
        self.instance.self_uri = test_value
        self.assertEqual(self.instance.self_uri, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Superevent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Superevent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Superevent.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

