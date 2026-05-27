"""
Test case for Superevent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gracedb_amqp_producer_data.org.ligo.gracedb.superevent import Superevent


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
            superevent_id='xuizkasygxjupedbeguo',
            category='cdowdiuqdkdjmzdcakmh',
            created='mazqtknaiugmnjahnqvy',
            t_start=float(25.838966486387715),
            t_0=float(69.72103677446714),
            t_end=float(64.07272820000426),
            far=float(69.08137124548274),
            time_coinc_far=float(5.009766067248423),
            space_coinc_far=float(84.46078454299688),
            labels_json='sttkryljpxejhrdepcen',
            preferred_event_id='ptwbxeprpgwdqsnfierm',
            pipeline='otjsysvgxrtlezahjuwr',
            group='lmzybfxmvahjsyovfrlt',
            instruments='osgmzcqdpvcntseepgov',
            gw_id='nmhticwbzkxzwsaldvju',
            submitter='rlktyufxvmxhymtxickr',
            em_type='suhmmgfysqscytzlvtjz',
            search='iclgnkfxvcijpeirspeb',
            far_is_upper_limit=True,
            nevents=int(23),
            self_uri='kyseddjmpffmvyoabrtq'
        )
        return instance

    
    def test_superevent_id_property(self):
        """
        Test superevent_id property
        """
        test_value = 'xuizkasygxjupedbeguo'
        self.instance.superevent_id = test_value
        self.assertEqual(self.instance.superevent_id, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = 'cdowdiuqdkdjmzdcakmh'
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_created_property(self):
        """
        Test created property
        """
        test_value = 'mazqtknaiugmnjahnqvy'
        self.instance.created = test_value
        self.assertEqual(self.instance.created, test_value)
    
    def test_t_start_property(self):
        """
        Test t_start property
        """
        test_value = float(25.838966486387715)
        self.instance.t_start = test_value
        self.assertEqual(self.instance.t_start, test_value)
    
    def test_t_0_property(self):
        """
        Test t_0 property
        """
        test_value = float(69.72103677446714)
        self.instance.t_0 = test_value
        self.assertEqual(self.instance.t_0, test_value)
    
    def test_t_end_property(self):
        """
        Test t_end property
        """
        test_value = float(64.07272820000426)
        self.instance.t_end = test_value
        self.assertEqual(self.instance.t_end, test_value)
    
    def test_far_property(self):
        """
        Test far property
        """
        test_value = float(69.08137124548274)
        self.instance.far = test_value
        self.assertEqual(self.instance.far, test_value)
    
    def test_time_coinc_far_property(self):
        """
        Test time_coinc_far property
        """
        test_value = float(5.009766067248423)
        self.instance.time_coinc_far = test_value
        self.assertEqual(self.instance.time_coinc_far, test_value)
    
    def test_space_coinc_far_property(self):
        """
        Test space_coinc_far property
        """
        test_value = float(84.46078454299688)
        self.instance.space_coinc_far = test_value
        self.assertEqual(self.instance.space_coinc_far, test_value)
    
    def test_labels_json_property(self):
        """
        Test labels_json property
        """
        test_value = 'sttkryljpxejhrdepcen'
        self.instance.labels_json = test_value
        self.assertEqual(self.instance.labels_json, test_value)
    
    def test_preferred_event_id_property(self):
        """
        Test preferred_event_id property
        """
        test_value = 'ptwbxeprpgwdqsnfierm'
        self.instance.preferred_event_id = test_value
        self.assertEqual(self.instance.preferred_event_id, test_value)
    
    def test_pipeline_property(self):
        """
        Test pipeline property
        """
        test_value = 'otjsysvgxrtlezahjuwr'
        self.instance.pipeline = test_value
        self.assertEqual(self.instance.pipeline, test_value)
    
    def test_group_property(self):
        """
        Test group property
        """
        test_value = 'lmzybfxmvahjsyovfrlt'
        self.instance.group = test_value
        self.assertEqual(self.instance.group, test_value)
    
    def test_instruments_property(self):
        """
        Test instruments property
        """
        test_value = 'osgmzcqdpvcntseepgov'
        self.instance.instruments = test_value
        self.assertEqual(self.instance.instruments, test_value)
    
    def test_gw_id_property(self):
        """
        Test gw_id property
        """
        test_value = 'nmhticwbzkxzwsaldvju'
        self.instance.gw_id = test_value
        self.assertEqual(self.instance.gw_id, test_value)
    
    def test_submitter_property(self):
        """
        Test submitter property
        """
        test_value = 'rlktyufxvmxhymtxickr'
        self.instance.submitter = test_value
        self.assertEqual(self.instance.submitter, test_value)
    
    def test_em_type_property(self):
        """
        Test em_type property
        """
        test_value = 'suhmmgfysqscytzlvtjz'
        self.instance.em_type = test_value
        self.assertEqual(self.instance.em_type, test_value)
    
    def test_search_property(self):
        """
        Test search property
        """
        test_value = 'iclgnkfxvcijpeirspeb'
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
        test_value = int(23)
        self.instance.nevents = test_value
        self.assertEqual(self.instance.nevents, test_value)
    
    def test_self_uri_property(self):
        """
        Test self_uri property
        """
        test_value = 'kyseddjmpffmvyoabrtq'
        self.instance.self_uri = test_value
        self.assertEqual(self.instance.self_uri, test_value)
    
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

