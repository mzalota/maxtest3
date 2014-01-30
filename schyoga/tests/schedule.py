from django.test import TestCase
from schyoga.bizobj.schedule import Schedule

import datetime

class TestSchedule(TestCase):

    def test_get_dates_for_week_1(self):
        #ARRANGE
        current_date = datetime.datetime(2014,1,29,15,35,44) #Wednesday, Jan 29, 2014 15:31:44
        week_start_date = datetime.datetime(2014,1,27,0,0,0) # midnight on Monday Jan 27, 2014
        week_end_date = datetime.datetime(2014,2,3,0,0,0) # midnight on Monday Feb 3, 2014

        #ACT
        start_date, end_date = Schedule.get_week_start_and_end_for_date(current_date)

        ##ASSERT
        self.assertIsNotNone(start_date)
        self.assertIsNotNone(end_date)
        self.assertEqual(start_date, week_start_date)
        self.assertEqual(end_date, week_end_date)


    def test_get_dates_for_week_2(self):
        #ARRANGE
        current_date = datetime.datetime(2005,1,1,15,35,44) #Wednesday, Jan 29, 2014 15:31:44
        week_start_date = datetime.datetime(2004,12,27,0,0,0) # midnight on Monday Jan 27, 2014
        week_end_date = datetime.datetime(2005,1,3,0,0,0) # midnight on Monday Feb 3, 2014

        #ACT
        start_date, end_date = Schedule.get_week_start_and_end_for_date(current_date)

        ##ASSERT
        self.assertIsNotNone(start_date)
        self.assertIsNotNone(end_date)
        self.assertEqual(start_date, week_start_date)
        self.assertEqual(end_date, week_end_date)

    def test_get_dates_for_week_3(self):
        #ARRANGE
        current_date = datetime.datetime(2010,1,3,15,35,44) #Wednesday, Jan 29, 2014 15:31:44
        week_start_date = datetime.datetime(2009,12,28,0,0,0) # midnight on Monday Jan 27, 2014
        week_end_date = datetime.datetime(2010,1,4,0,0,0) # midnight on Monday Feb 3, 2014

        #ACT
        start_date, end_date = Schedule.get_week_start_and_end_for_date(current_date)

        ##ASSERT
        self.assertIsNotNone(start_date)
        self.assertIsNotNone(end_date)
        self.assertEqual(start_date, week_start_date)
        self.assertEqual(end_date, week_end_date)


    def test_get_dates_for_week_4(self):
        #ARRANGE
        current_date = datetime.datetime(2010,1,4,15,35,44) #Wednesday, Jan 29, 2014 15:31:44
        week_start_date = datetime.datetime(2010,1,4,0,0,0) # midnight on Monday Jan 27, 2014
        week_end_date = datetime.datetime(2010,1,11,0,0,0) # midnight on Monday Feb 3, 2014

        #ACT
        start_date, end_date = Schedule.get_week_start_and_end_for_date(current_date)

        ##ASSERT
        self.assertIsNotNone(start_date)
        self.assertIsNotNone(end_date)
        self.assertEqual(start_date, week_start_date)
        self.assertEqual(end_date, week_end_date)

    #def test_get_dates_for_week2(self):
    #    #ARRANGE

    #    #ACT
    #    start_date1, end_date1 = Schedule.get_week_start_and_end_for_week(2005,1)
    #    start_date2, end_date2 = Schedule.get_week_start_and_end_for_week(2010,1)
    #    start_date3, end_date3 = Schedule.get_week_start_and_end_for_week(2009,53)
    #
    #    ##ASSERT
    #    self.assertEqual(start_date1, datetime.datetime(2004,12,27,0,0,0))
    #    self.assertEqual(start_date2, datetime.datetime(2010,1,4,0,0,0))
    #    self.assertEqual(start_date3, datetime.datetime(2009,1,28,0,0,0))


#
#>>> iso = datetime.date(2005, 1, 1).isocalendar()
#>>> iso
#(2004, 53, 6)
#>>> iso_to_gregorian(*iso)
#datetime.date(2005, 1, 1)
#
#>>> iso = datetime.date(2010, 1, 4).isocalendar()
#>>> iso
#(2010, 1, 1)
#>>> iso_to_gregorian(*iso)
#datetime.date(2010, 1, 4)
#
#>>> iso = datetime.date(2010, 1, 3).isocalendar()
#>>> iso
#(2009, 53, 7)
#>>> iso_to_gregorian(*iso)
#datetime.date(2010, 1, 3)