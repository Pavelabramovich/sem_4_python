import unittest
from datetime import date, time, datetime, timedelta
from unittest import TestCase
from SerializationOfClassesAndFuncs import SerializersFactory, Serialization

from tests.objects_for_test import B


class TestSerializersFactory(TestCase):
    def setUp(self):
        self.factory = SerializersFactory

    def test_json(self):
        serializer = self.factory.create_serializer(Serialization.JSON)

        sB = serializer.dumps(B)
        sB = serializer.loads(sB)

        self.assertEqual(B.bx_test(), sB.bx_test())

    def test_xml(self):
        serializer = self.factory.create_serializer(Serialization.XML)

        sB = serializer.dumps(B)
        sB = serializer.loads(sB)

        self.assertEqual(B.bx_test(), sB.bx_test())

    def test_json_str(self):
        serializer = self.factory.create_serializer('json')

        sB = serializer.dumps(B)
        sB = serializer.loads(sB)

        self.assertEqual(B.bx_test(), sB.bx_test())

    def test_xml_str(self):
        serializer = self.factory.create_serializer('xml')

        sB = serializer.dumps(B)
        sB = serializer.loads(sB)

        self.assertEqual(B.bx_test(), sB.bx_test())

    def test_jumble(self):
        with self.assertRaises(ValueError):
            serializer = self.factory.create_serializer("12345fdgawzsg")

