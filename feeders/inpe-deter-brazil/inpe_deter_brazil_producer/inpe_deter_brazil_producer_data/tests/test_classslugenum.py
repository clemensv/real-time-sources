import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from inpe_deter_brazil_producer_data.br.inpe.deter.classslugenum import ClassSlugenum


class Test_ClassSlugenum(unittest.TestCase):
    """
    Test case for ClassSlugenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ClassSlugenum.desmatamento_cr

    @staticmethod
    def create_instance():
        """
        Create instance of ClassSlugenum
        """
        return ClassSlugenum.desmatamento_cr

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ClassSlugenum.desmatamento_cr.value, 'desmatamento-cr')
        self.assertEqual(ClassSlugenum.desmatamento_veg.value, 'desmatamento-veg')
        self.assertEqual(ClassSlugenum.degradacao.value, 'degradacao')
        self.assertEqual(ClassSlugenum.mineracao.value, 'mineracao')
        self.assertEqual(ClassSlugenum.cs_desordenado.value, 'cs-desordenado')
        self.assertEqual(ClassSlugenum.cs_geometrico.value, 'cs-geometrico')
        self.assertEqual(ClassSlugenum.cicatriz_de_queimada.value, 'cicatriz-de-queimada')
        self.assertEqual(ClassSlugenum.corte_seletivo.value, 'corte-seletivo')
        self.assertEqual(ClassSlugenum.unknown.value, 'unknown')