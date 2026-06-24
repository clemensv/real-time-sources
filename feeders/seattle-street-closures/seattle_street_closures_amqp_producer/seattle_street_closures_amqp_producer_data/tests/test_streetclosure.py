"""
Test case for StreetClosure
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from seattle_street_closures_amqp_producer_data.streetclosure import StreetClosure


class Test_StreetClosure(unittest.TestCase):
    """
    Test case for StreetClosure
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StreetClosure.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StreetClosure for testing
        """
        instance = StreetClosure(
            closure_id='kmfldzzjfdymxirscjmq',
            permit_number='npovzevnundtpqmadzja',
            permit_type='rfjcjbjdjbpxcymbfpey',
            project_name='hufabfazdbzmgowkblcv',
            project_description='nlcjnwhogobadogixdym',
            start_date='tqyxhesfggmoelutpdwn',
            end_date='ilibxquwmyzewazqhopu',
            sunday='dohhxnyozmtxtvtjotpl',
            monday='opqekizzthoqkgsslctt',
            tuesday='kvchnrixmsedlcwpwgmh',
            wednesday='cjazzvozojptiqgpddnd',
            thursday='wadnnppwbngmivelbzyq',
            friday='dbdvifrqmjubisbxdsps',
            saturday='lstizlyxtnudoiaxymqj',
            street_on='xfknherjbvmjnwtxyrfc',
            street_from='paqyneonqietqshajjhk',
            street_to='mbjcmljrxtdpqkdqfzou',
            segkey='npniscmtlpzbtprnjatc',
            geometry_json='cuootbedmdxgxzlwhvis'
        )
        return instance

    
    def test_closure_id_property(self):
        """
        Test closure_id property
        """
        test_value = 'kmfldzzjfdymxirscjmq'
        self.instance.closure_id = test_value
        self.assertEqual(self.instance.closure_id, test_value)
    
    def test_permit_number_property(self):
        """
        Test permit_number property
        """
        test_value = 'npovzevnundtpqmadzja'
        self.instance.permit_number = test_value
        self.assertEqual(self.instance.permit_number, test_value)
    
    def test_permit_type_property(self):
        """
        Test permit_type property
        """
        test_value = 'rfjcjbjdjbpxcymbfpey'
        self.instance.permit_type = test_value
        self.assertEqual(self.instance.permit_type, test_value)
    
    def test_project_name_property(self):
        """
        Test project_name property
        """
        test_value = 'hufabfazdbzmgowkblcv'
        self.instance.project_name = test_value
        self.assertEqual(self.instance.project_name, test_value)
    
    def test_project_description_property(self):
        """
        Test project_description property
        """
        test_value = 'nlcjnwhogobadogixdym'
        self.instance.project_description = test_value
        self.assertEqual(self.instance.project_description, test_value)
    
    def test_start_date_property(self):
        """
        Test start_date property
        """
        test_value = 'tqyxhesfggmoelutpdwn'
        self.instance.start_date = test_value
        self.assertEqual(self.instance.start_date, test_value)
    
    def test_end_date_property(self):
        """
        Test end_date property
        """
        test_value = 'ilibxquwmyzewazqhopu'
        self.instance.end_date = test_value
        self.assertEqual(self.instance.end_date, test_value)
    
    def test_sunday_property(self):
        """
        Test sunday property
        """
        test_value = 'dohhxnyozmtxtvtjotpl'
        self.instance.sunday = test_value
        self.assertEqual(self.instance.sunday, test_value)
    
    def test_monday_property(self):
        """
        Test monday property
        """
        test_value = 'opqekizzthoqkgsslctt'
        self.instance.monday = test_value
        self.assertEqual(self.instance.monday, test_value)
    
    def test_tuesday_property(self):
        """
        Test tuesday property
        """
        test_value = 'kvchnrixmsedlcwpwgmh'
        self.instance.tuesday = test_value
        self.assertEqual(self.instance.tuesday, test_value)
    
    def test_wednesday_property(self):
        """
        Test wednesday property
        """
        test_value = 'cjazzvozojptiqgpddnd'
        self.instance.wednesday = test_value
        self.assertEqual(self.instance.wednesday, test_value)
    
    def test_thursday_property(self):
        """
        Test thursday property
        """
        test_value = 'wadnnppwbngmivelbzyq'
        self.instance.thursday = test_value
        self.assertEqual(self.instance.thursday, test_value)
    
    def test_friday_property(self):
        """
        Test friday property
        """
        test_value = 'dbdvifrqmjubisbxdsps'
        self.instance.friday = test_value
        self.assertEqual(self.instance.friday, test_value)
    
    def test_saturday_property(self):
        """
        Test saturday property
        """
        test_value = 'lstizlyxtnudoiaxymqj'
        self.instance.saturday = test_value
        self.assertEqual(self.instance.saturday, test_value)
    
    def test_street_on_property(self):
        """
        Test street_on property
        """
        test_value = 'xfknherjbvmjnwtxyrfc'
        self.instance.street_on = test_value
        self.assertEqual(self.instance.street_on, test_value)
    
    def test_street_from_property(self):
        """
        Test street_from property
        """
        test_value = 'paqyneonqietqshajjhk'
        self.instance.street_from = test_value
        self.assertEqual(self.instance.street_from, test_value)
    
    def test_street_to_property(self):
        """
        Test street_to property
        """
        test_value = 'mbjcmljrxtdpqkdqfzou'
        self.instance.street_to = test_value
        self.assertEqual(self.instance.street_to, test_value)
    
    def test_segkey_property(self):
        """
        Test segkey property
        """
        test_value = 'npniscmtlpzbtprnjatc'
        self.instance.segkey = test_value
        self.assertEqual(self.instance.segkey, test_value)
    
    def test_geometry_json_property(self):
        """
        Test geometry_json property
        """
        test_value = 'cuootbedmdxgxzlwhvis'
        self.instance.geometry_json = test_value
        self.assertEqual(self.instance.geometry_json, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StreetClosure.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StreetClosure.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

