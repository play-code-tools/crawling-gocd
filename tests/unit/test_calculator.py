import unittest
from unittest.mock import Mock
from crawling_gocd.calculator import Calculator
from crawling_gocd.calculate_domain import CalculateStrategyHandler


class CaculatorTest(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator([Mock(spec=CalculateStrategyHandler)])

    def test_should_invoking_handler_work_correctly(self):
        self.calculator.work([])
        self.calculator.strategyHandlers[0].calculate.assert_called_once_with([], [])

