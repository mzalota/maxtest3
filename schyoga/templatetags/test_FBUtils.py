#from unittest import TestCase
import unittest
import pytz

#import schyoga.templatetags

from schyoga.templatetags.maxcustomfilter1 import FBUtils

import datetime


class TestFBUtils(unittest.TestCase):
    def test_convertString2Date_happyPath1(self):
        #arrange
        testDateStr = '2010-07-25T19:46:27+0000'
        fbUtils = FBUtils()

        #act
        dtObj = fbUtils.convertString2Date(testDateStr)

        #assert
        self.assertIsNotNone(dtObj)
        self.assertIsInstance(dtObj, datetime.datetime)
        self.assertEqual(dtObj.year, 2010)
        self.assertEqual(dtObj.month, 7)
        self.assertEqual(dtObj.day, 25)
        self.assertEqual(dtObj.hour, 19)
        self.assertEqual(dtObj.minute, 46)
        self.assertEqual(dtObj.second, 27)
        self.assertEqual(dtObj.tzname() , 'UTC')

    def test_convertString2Date_otherTimeZoneMinus(self):
        #arrange
        testDateStr = '2010-07-25T22:46:27-0600'
        fbUtils = FBUtils()

        #act
        dtObj = fbUtils.convertString2Date(testDateStr)

        #assert
        self.assertIsNotNone(dtObj)
        self.assertIsInstance(dtObj, datetime.datetime)
        self.assertEqual(dtObj.hour, 4)
        self.assertEqual(dtObj.day, 26)
        self.assertEqual(dtObj.tzname() , 'UTC')


    def test_convertString2Date_otherTimeZonePlus(self):
        #arrange
        testDateStr = '2010-07-25T03:46:27+1032'
        fbUtils = FBUtils()

        #act
        dtObj = fbUtils.convertString2Date(testDateStr)

        #assert
        self.assertIsNotNone(dtObj)
        self.assertIsInstance(dtObj, datetime.datetime)
        self.assertEqual(dtObj.minute, 14)
        self.assertEqual(dtObj.hour, 17)
        self.assertEqual(dtObj.day, 24)
        self.assertEqual(dtObj.tzname() , 'UTC')

    def test_convertString2Date_invalidTimeZone(self):
        #arrange
        testDateStr = '2010-07-25T03:46:27EST'
        fbUtils = FBUtils()

        #act and assert
        self.assertRaises(ValueError,  fbUtils.convertString2Date, (testDateStr))

    def test_convertString2Date_invaliDate(self):

        #arrange
        testDateStr = '2010_07_25T03:46:27EST'
        fbUtils = FBUtils()

        #act and assert
        self.assertRaises(ValueError,  fbUtils.convertString2Date, (testDateStr))
