"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from unittest import TestCase

#from django.test import TestCase
from schyoga.bizobj.state import State


class TestState(TestCase):
    def test_createValid(self):
        #ARRANGE
        testStateName = 'rhode-island'

        #ACT
        stateObj = State.createFromUrlName(testStateName)

        #ASSERT
        self.assertIsNotNone(stateObj)

    def test_createValidWithLeadingAndTrailingSpaces(self):
        #ARRANGE
        testStateName = '  rhode-island  '

        #ACT
        stateObj = State.createFromUrlName(testStateName)

        #ASSERT
        self.assertIsNotNone(stateObj)


    def test_stateName(self):
        #ARRANGE
        testStateName = '  rhode-island '
        stateObj = State.createFromUrlName(testStateName)

        #ACT
        stateName = stateObj.name

        #ASSERT
        self.assertEqual("Rhode Island", stateName)


    def test_createWithInvalidString(self):
        #ARRANGE
        testStateName = 'rhode'

        #ACT
        stateObj = State.createFromUrlName(testStateName)

        #ASSERT
        self.assertIsNone(stateObj)



"""
class SimpleDiangoTest(TestCase):
    def test_basic_addition(self):

        #Tests that 1 + 1 always equals 2.

        self.assertEqual(1 + 1, 2)
"""


