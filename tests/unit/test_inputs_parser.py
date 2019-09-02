import unittest
import json
from crawling_gocd.inputs_parser import InputsParser 

class InputsParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = InputsParser("tests/unit/resources/inputs.yaml")

    def test_should_generate_inputs_object_correctly(self):
        result = self.parser.parse()
        self.assertGreater(len(result), 0)
        