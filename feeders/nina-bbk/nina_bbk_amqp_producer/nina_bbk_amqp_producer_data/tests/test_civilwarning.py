"""
Test case for CivilWarning
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nina_bbk_amqp_producer_data.civilwarning import CivilWarning
from nina_bbk_amqp_producer_data.providerenum import ProviderEnum
from nina_bbk_amqp_producer_data.urgencyenum import UrgencyEnum
from nina_bbk_amqp_producer_data.certaintyenum import CertaintyEnum
from nina_bbk_amqp_producer_data.categoryenum import CategoryEnum
from nina_bbk_amqp_producer_data.scopeenum import ScopeEnum
from nina_bbk_amqp_producer_data.msgtypeenum import MsgTypeenum
from nina_bbk_amqp_producer_data.statusenum import StatusEnum
from nina_bbk_amqp_producer_data.severityenum import SeverityEnum
import datetime


class Test_CivilWarning(unittest.TestCase):
    """
    Test case for CivilWarning
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CivilWarning.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CivilWarning for testing
        """
        instance = CivilWarning(
            warning_id='govewjniybfiklvmqblx',
            provider=ProviderEnum.mowas,
            version=int(90),
            sender='rzbxofiovlzkovkupqxr',
            sender_name='etnimzblarrzsrapqyty',
            sent=datetime.datetime.now(datetime.timezone.utc),
            status=StatusEnum.Actual,
            msg_type=MsgTypeenum.Alert,
            scope=ScopeEnum.Public,
            references='ypczjnnqkfqvufidplxz',
            event='dmuaototxuqstitwyofr',
            event_code='ydbuwezdznjqollcaeip',
            category=CategoryEnum.Met,
            severity=SeverityEnum.Extreme,
            urgency=UrgencyEnum.Immediate,
            certainty=CertaintyEnum.Observed,
            headline='iqxjclufrdrwpzvmiiyu',
            description='gkyhtqpzkwyorushzbnm',
            instruction='vozuintapsslwvdskvzc',
            web='vdpabqdwqqshufulnodb',
            contact='spjduuczickcxzcvlpem',
            area_desc='yyqsthpeufkedfxsxoos',
            verwaltungsbereiche='eydndijdymlqkynjippf',
            language='asucfuwkroheuiquqtjb',
            state='yuuriyyvaeqpbpbcrnto'
        )
        return instance

    
    def test_warning_id_property(self):
        """
        Test warning_id property
        """
        test_value = 'govewjniybfiklvmqblx'
        self.instance.warning_id = test_value
        self.assertEqual(self.instance.warning_id, test_value)
    
    def test_provider_property(self):
        """
        Test provider property
        """
        test_value = ProviderEnum.mowas
        self.instance.provider = test_value
        self.assertEqual(self.instance.provider, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = int(90)
        self.instance.version = test_value
        self.assertEqual(self.instance.version, test_value)
    
    def test_sender_property(self):
        """
        Test sender property
        """
        test_value = 'rzbxofiovlzkovkupqxr'
        self.instance.sender = test_value
        self.assertEqual(self.instance.sender, test_value)
    
    def test_sender_name_property(self):
        """
        Test sender_name property
        """
        test_value = 'etnimzblarrzsrapqyty'
        self.instance.sender_name = test_value
        self.assertEqual(self.instance.sender_name, test_value)
    
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
    
    def test_scope_property(self):
        """
        Test scope property
        """
        test_value = ScopeEnum.Public
        self.instance.scope = test_value
        self.assertEqual(self.instance.scope, test_value)
    
    def test_references_property(self):
        """
        Test references property
        """
        test_value = 'ypczjnnqkfqvufidplxz'
        self.instance.references = test_value
        self.assertEqual(self.instance.references, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = 'dmuaototxuqstitwyofr'
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
    def test_event_code_property(self):
        """
        Test event_code property
        """
        test_value = 'ydbuwezdznjqollcaeip'
        self.instance.event_code = test_value
        self.assertEqual(self.instance.event_code, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = CategoryEnum.Met
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = SeverityEnum.Extreme
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_urgency_property(self):
        """
        Test urgency property
        """
        test_value = UrgencyEnum.Immediate
        self.instance.urgency = test_value
        self.assertEqual(self.instance.urgency, test_value)
    
    def test_certainty_property(self):
        """
        Test certainty property
        """
        test_value = CertaintyEnum.Observed
        self.instance.certainty = test_value
        self.assertEqual(self.instance.certainty, test_value)
    
    def test_headline_property(self):
        """
        Test headline property
        """
        test_value = 'iqxjclufrdrwpzvmiiyu'
        self.instance.headline = test_value
        self.assertEqual(self.instance.headline, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'gkyhtqpzkwyorushzbnm'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_instruction_property(self):
        """
        Test instruction property
        """
        test_value = 'vozuintapsslwvdskvzc'
        self.instance.instruction = test_value
        self.assertEqual(self.instance.instruction, test_value)
    
    def test_web_property(self):
        """
        Test web property
        """
        test_value = 'vdpabqdwqqshufulnodb'
        self.instance.web = test_value
        self.assertEqual(self.instance.web, test_value)
    
    def test_contact_property(self):
        """
        Test contact property
        """
        test_value = 'spjduuczickcxzcvlpem'
        self.instance.contact = test_value
        self.assertEqual(self.instance.contact, test_value)
    
    def test_area_desc_property(self):
        """
        Test area_desc property
        """
        test_value = 'yyqsthpeufkedfxsxoos'
        self.instance.area_desc = test_value
        self.assertEqual(self.instance.area_desc, test_value)
    
    def test_verwaltungsbereiche_property(self):
        """
        Test verwaltungsbereiche property
        """
        test_value = 'eydndijdymlqkynjippf'
        self.instance.verwaltungsbereiche = test_value
        self.assertEqual(self.instance.verwaltungsbereiche, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'asucfuwkroheuiquqtjb'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'yuuriyyvaeqpbpbcrnto'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CivilWarning.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = CivilWarning.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

