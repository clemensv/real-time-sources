"""
Test case for CapAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cap_alerts_amqp_producer_data.org.oasis.cap.alerts.capalert import CapAlert
from cap_alerts_amqp_producer_data.org.oasis.cap.alerts.valuepair import ValuePair
from cap_alerts_amqp_producer_data.org.oasis.cap.alerts.statusenum import StatusEnum
from cap_alerts_amqp_producer_data.org.oasis.cap.alerts.msgtypeenum import MsgTypeenum
from cap_alerts_amqp_producer_data.org.oasis.cap.alerts.scopeenum import ScopeEnum
from cap_alerts_amqp_producer_data.org.oasis.cap.alerts.capinfo import CapInfo
import datetime


class Test_CapAlert(unittest.TestCase):
    """
    Test case for CapAlert
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CapAlert.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CapAlert for testing
        """
        instance = CapAlert(
            cap_source_id='mhtnfmwsczyacucbhwla',
            identifier='nwehcdlwhqptvffvuokr',
            sender='afhrqosfugcdjqtnktyk',
            sent=datetime.datetime.now(datetime.timezone.utc),
            status=StatusEnum.Actual,
            msg_type=MsgTypeenum.Alert,
            source='fmrfnfuoejzvdmfotifz',
            scope=ScopeEnum.Public,
            restriction='erwyyunyezvctmrsmpca',
            addresses=['akrzebgwthvsultoduhx', 'mcxsoiototvinpqxpfjw', 'bfhcgtxqzentkdayocbe', 'pwwakvzqzgezhehcgrwh', 'lqgsevpyhpvnjjzawvlo'],
            code=[None, None, None, None],
            note='wchievnyhywkfkvebari',
            references=['cqhosmnytgwhwgmodjve', 'baohxwfcmrzxagbrxnhj'],
            incidents=['jdrcfsewbpuluxhkxgmo', 'zerklzevkpozpnfnteld'],
            info=[None, None],
            provider_url='jssusuqxrtgdmttfzobw',
            raw_cap_xml='mjfaoxwsqoyprkhguccv',
            area_desc='jaisiriiobowxxepyjkn',
            same_codes=['ncmglllrtzxeteosvruv', 'mnjqpntndngwedmqtlcc'],
            ugc_codes=['uuczyhwaflktwnctvoxx'],
            vtec=['dcmfgqgyxsxrjutfjfmp', 'fhvwmpnefofsrdhwkzgl', 'qqrhpgrtzeibsxbrllia', 'cdmktcmqmhcbydggdsyx', 'hfipmypbddurqadcpsse'],
            awareness_level='oqolatlovqzrvlosacpn',
            awareness_type='upaeuhdtsqgvedsyqbjk',
            event_type='vzrfmcsupcvbyjysvcit',
            state='tupbhtikpsylnobfaflr',
            affected_zones=['poeihseddplducrwnyhk', 'vokslotukhggxbmnadyu', 'vxrotffrtdskqhkeznni', 'pxjnpufxsyculxbjakbh'],
            raw_source_json='xnrxrpgiizbggtvypjta'
        )
        return instance

    
    def test_cap_source_id_property(self):
        """
        Test cap_source_id property
        """
        test_value = 'mhtnfmwsczyacucbhwla'
        self.instance.cap_source_id = test_value
        self.assertEqual(self.instance.cap_source_id, test_value)
    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'nwehcdlwhqptvffvuokr'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_sender_property(self):
        """
        Test sender property
        """
        test_value = 'afhrqosfugcdjqtnktyk'
        self.instance.sender = test_value
        self.assertEqual(self.instance.sender, test_value)
    
    def test_sent_property(self):
        """
        Test sent property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.sent = test_value
        self.assertEqual(self.instance.sent, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = StatusEnum.Actual
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = MsgTypeenum.Alert
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_source_property(self):
        """
        Test source property
        """
        test_value = 'fmrfnfuoejzvdmfotifz'
        self.instance.source = test_value
        self.assertEqual(self.instance.source, test_value)
    
    def test_scope_property(self):
        """
        Test scope property
        """
        test_value = ScopeEnum.Public
        self.instance.scope = test_value
        self.assertEqual(self.instance.scope, test_value)
    
    def test_restriction_property(self):
        """
        Test restriction property
        """
        test_value = 'erwyyunyezvctmrsmpca'
        self.instance.restriction = test_value
        self.assertEqual(self.instance.restriction, test_value)
    
    def test_addresses_property(self):
        """
        Test addresses property
        """
        test_value = ['akrzebgwthvsultoduhx', 'mcxsoiototvinpqxpfjw', 'bfhcgtxqzentkdayocbe', 'pwwakvzqzgezhehcgrwh', 'lqgsevpyhpvnjjzawvlo']
        self.instance.addresses = test_value
        self.assertEqual(self.instance.addresses, test_value)
    
    def test_code_property(self):
        """
        Test code property
        """
        test_value = [None, None, None, None]
        self.instance.code = test_value
        self.assertEqual(self.instance.code, test_value)
    
    def test_note_property(self):
        """
        Test note property
        """
        test_value = 'wchievnyhywkfkvebari'
        self.instance.note = test_value
        self.assertEqual(self.instance.note, test_value)
    
    def test_references_property(self):
        """
        Test references property
        """
        test_value = ['cqhosmnytgwhwgmodjve', 'baohxwfcmrzxagbrxnhj']
        self.instance.references = test_value
        self.assertEqual(self.instance.references, test_value)
    
    def test_incidents_property(self):
        """
        Test incidents property
        """
        test_value = ['jdrcfsewbpuluxhkxgmo', 'zerklzevkpozpnfnteld']
        self.instance.incidents = test_value
        self.assertEqual(self.instance.incidents, test_value)
    
    def test_info_property(self):
        """
        Test info property
        """
        test_value = [None, None]
        self.instance.info = test_value
        self.assertEqual(self.instance.info, test_value)
    
    def test_provider_url_property(self):
        """
        Test provider_url property
        """
        test_value = 'jssusuqxrtgdmttfzobw'
        self.instance.provider_url = test_value
        self.assertEqual(self.instance.provider_url, test_value)
    
    def test_raw_cap_xml_property(self):
        """
        Test raw_cap_xml property
        """
        test_value = 'mjfaoxwsqoyprkhguccv'
        self.instance.raw_cap_xml = test_value
        self.assertEqual(self.instance.raw_cap_xml, test_value)
    
    def test_area_desc_property(self):
        """
        Test area_desc property
        """
        test_value = 'jaisiriiobowxxepyjkn'
        self.instance.area_desc = test_value
        self.assertEqual(self.instance.area_desc, test_value)
    
    def test_same_codes_property(self):
        """
        Test same_codes property
        """
        test_value = ['ncmglllrtzxeteosvruv', 'mnjqpntndngwedmqtlcc']
        self.instance.same_codes = test_value
        self.assertEqual(self.instance.same_codes, test_value)
    
    def test_ugc_codes_property(self):
        """
        Test ugc_codes property
        """
        test_value = ['uuczyhwaflktwnctvoxx']
        self.instance.ugc_codes = test_value
        self.assertEqual(self.instance.ugc_codes, test_value)
    
    def test_vtec_property(self):
        """
        Test vtec property
        """
        test_value = ['dcmfgqgyxsxrjutfjfmp', 'fhvwmpnefofsrdhwkzgl', 'qqrhpgrtzeibsxbrllia', 'cdmktcmqmhcbydggdsyx', 'hfipmypbddurqadcpsse']
        self.instance.vtec = test_value
        self.assertEqual(self.instance.vtec, test_value)
    
    def test_awareness_level_property(self):
        """
        Test awareness_level property
        """
        test_value = 'oqolatlovqzrvlosacpn'
        self.instance.awareness_level = test_value
        self.assertEqual(self.instance.awareness_level, test_value)
    
    def test_awareness_type_property(self):
        """
        Test awareness_type property
        """
        test_value = 'upaeuhdtsqgvedsyqbjk'
        self.instance.awareness_type = test_value
        self.assertEqual(self.instance.awareness_type, test_value)
    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = 'vzrfmcsupcvbyjysvcit'
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'tupbhtikpsylnobfaflr'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_affected_zones_property(self):
        """
        Test affected_zones property
        """
        test_value = ['poeihseddplducrwnyhk', 'vokslotukhggxbmnadyu', 'vxrotffrtdskqhkeznni', 'pxjnpufxsyculxbjakbh']
        self.instance.affected_zones = test_value
        self.assertEqual(self.instance.affected_zones, test_value)
    
    def test_raw_source_json_property(self):
        """
        Test raw_source_json property
        """
        test_value = 'xnrxrpgiizbggtvypjta'
        self.instance.raw_source_json = test_value
        self.assertEqual(self.instance.raw_source_json, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CapAlert.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = CapAlert.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

