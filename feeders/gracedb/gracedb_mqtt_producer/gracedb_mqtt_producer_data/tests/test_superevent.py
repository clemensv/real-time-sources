"""
Test case for Superevent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gracedb_mqtt_producer_data.org.ligo.gracedb.superevent import Superevent


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
            superevent_id='dpwzlubgtqyocshswoad',
            category='cugexbrcybqiopswqzfz',
            created='eozbervyqauljdenfmbt',
            t_start=float(46.00731348834702),
            t_0=float(6.216539142067323),
            t_end=float(95.98859572815056),
            far=float(45.09366332126189),
            time_coinc_far=float(43.187109628862345),
            space_coinc_far=float(30.252769065132558),
            labels_json='pbdwctllumbedaplukcu',
            preferred_event_id='ifuumbcvfvbethugjyya',
            pipeline='terdydltawvbgwbcluiu',
            group='iepmiahtstflnusffncn',
            instruments='jkebjgyrxqxcwchxrosa',
            gw_id='bntseqmxfiaythguxzcb',
            submitter='jdkfnamjvfydlrwlyskq',
            em_type='mmdylpcuxcsfnwzsamhu',
            search='herllsvzdhlenfrftroq',
            far_is_upper_limit=False,
            nevents=int(37),
            self_uri='wbyhxvmfzhjlsxzmrcmq'
        )
        return instance

    
    def test_superevent_id_property(self):
        """
        Test superevent_id property
        """
        test_value = 'dpwzlubgtqyocshswoad'
        self.instance.superevent_id = test_value
        self.assertEqual(self.instance.superevent_id, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = 'cugexbrcybqiopswqzfz'
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_created_property(self):
        """
        Test created property
        """
        test_value = 'eozbervyqauljdenfmbt'
        self.instance.created = test_value
        self.assertEqual(self.instance.created, test_value)
    
    def test_t_start_property(self):
        """
        Test t_start property
        """
        test_value = float(46.00731348834702)
        self.instance.t_start = test_value
        self.assertEqual(self.instance.t_start, test_value)
    
    def test_t_0_property(self):
        """
        Test t_0 property
        """
        test_value = float(6.216539142067323)
        self.instance.t_0 = test_value
        self.assertEqual(self.instance.t_0, test_value)
    
    def test_t_end_property(self):
        """
        Test t_end property
        """
        test_value = float(95.98859572815056)
        self.instance.t_end = test_value
        self.assertEqual(self.instance.t_end, test_value)
    
    def test_far_property(self):
        """
        Test far property
        """
        test_value = float(45.09366332126189)
        self.instance.far = test_value
        self.assertEqual(self.instance.far, test_value)
    
    def test_time_coinc_far_property(self):
        """
        Test time_coinc_far property
        """
        test_value = float(43.187109628862345)
        self.instance.time_coinc_far = test_value
        self.assertEqual(self.instance.time_coinc_far, test_value)
    
    def test_space_coinc_far_property(self):
        """
        Test space_coinc_far property
        """
        test_value = float(30.252769065132558)
        self.instance.space_coinc_far = test_value
        self.assertEqual(self.instance.space_coinc_far, test_value)
    
    def test_labels_json_property(self):
        """
        Test labels_json property
        """
        test_value = 'pbdwctllumbedaplukcu'
        self.instance.labels_json = test_value
        self.assertEqual(self.instance.labels_json, test_value)
    
    def test_preferred_event_id_property(self):
        """
        Test preferred_event_id property
        """
        test_value = 'ifuumbcvfvbethugjyya'
        self.instance.preferred_event_id = test_value
        self.assertEqual(self.instance.preferred_event_id, test_value)
    
    def test_pipeline_property(self):
        """
        Test pipeline property
        """
        test_value = 'terdydltawvbgwbcluiu'
        self.instance.pipeline = test_value
        self.assertEqual(self.instance.pipeline, test_value)
    
    def test_group_property(self):
        """
        Test group property
        """
        test_value = 'iepmiahtstflnusffncn'
        self.instance.group = test_value
        self.assertEqual(self.instance.group, test_value)
    
    def test_instruments_property(self):
        """
        Test instruments property
        """
        test_value = 'jkebjgyrxqxcwchxrosa'
        self.instance.instruments = test_value
        self.assertEqual(self.instance.instruments, test_value)
    
    def test_gw_id_property(self):
        """
        Test gw_id property
        """
        test_value = 'bntseqmxfiaythguxzcb'
        self.instance.gw_id = test_value
        self.assertEqual(self.instance.gw_id, test_value)
    
    def test_submitter_property(self):
        """
        Test submitter property
        """
        test_value = 'jdkfnamjvfydlrwlyskq'
        self.instance.submitter = test_value
        self.assertEqual(self.instance.submitter, test_value)
    
    def test_em_type_property(self):
        """
        Test em_type property
        """
        test_value = 'mmdylpcuxcsfnwzsamhu'
        self.instance.em_type = test_value
        self.assertEqual(self.instance.em_type, test_value)
    
    def test_search_property(self):
        """
        Test search property
        """
        test_value = 'herllsvzdhlenfrftroq'
        self.instance.search = test_value
        self.assertEqual(self.instance.search, test_value)
    
    def test_far_is_upper_limit_property(self):
        """
        Test far_is_upper_limit property
        """
        test_value = False
        self.instance.far_is_upper_limit = test_value
        self.assertEqual(self.instance.far_is_upper_limit, test_value)
    
    def test_nevents_property(self):
        """
        Test nevents property
        """
        test_value = int(37)
        self.instance.nevents = test_value
        self.assertEqual(self.instance.nevents, test_value)
    
    def test_self_uri_property(self):
        """
        Test self_uri property
        """
        test_value = 'wbyhxvmfzhjlsxzmrcmq'
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

