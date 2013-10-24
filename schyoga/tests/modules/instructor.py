from time import sleep
from unittest import TestCase
from mock import patch
from schyoga.models import Instructor, Studio


class TestInstructor(TestCase):

    def test_saving_alias_as_list(self):
        #ARRANGE
        list_of_aliases = list(["value1", "value2"])
        #ACT
        newObj = Instructor()
        newObj.aliases_list = list_of_aliases
        newObj.save()
        id = newObj.id

        #ASSERT
        self.assertIsNotNone(id)

        #ACT 2
        fetchObj = Instructor.objects.get(pk=id)

        #ASSERT 2
        self.assertIsNotNone(fetchObj)
        self.assertListEqual(fetchObj.aliases_list, list_of_aliases)
        sleep(20)

    #TODO: read Django Best Practices http://blog.apps.chicagotribune.com/2010/02/26/best-practices/

    def test_clean_up_name(self):
        #ARRANGE
        name_1_raw = u'Leslie Lewis (3)'
        name_1_expected = 'Leslie Lewis'

        name_2_raw = 'Leslie Lewis (3)'
        name_2_expected = 'Leslie Lewis'

        name_3_raw = u' lulu   ekiert '
        name_3_expected = u'Lulu Ekiert'

        name_4_raw = u'Aimee McCabe - Karr'
        name_4_expected = u'Aimee McCabe - Karr'

        name_5_raw = u"Carrie Gaynor @ 520 Packett's Landing"
        name_5_expected = u'Carrie Gaynor'

        name_6_raw = u"  "
        name_6_expected = u''

        #ACT
        name_1_clean = Instructor.clean_up_name(name_1_raw)
        name_2_clean = Instructor.clean_up_name(name_2_raw)
        name_3_clean = Instructor.clean_up_name(name_3_raw)
        name_4_clean = Instructor.clean_up_name(name_4_raw)
        name_5_clean = Instructor.clean_up_name(name_5_raw)
        name_6_clean = Instructor.clean_up_name(name_6_raw)

        #ASSERT
        self.assertEqual(name_1_clean, name_1_expected)
        self.assertEqual(name_2_clean, name_2_expected)
        self.assertEqual(name_3_clean, name_3_expected)
        self.assertEqual(name_4_clean, name_4_expected)
        self.assertEqual(name_5_clean, name_5_expected)
        self.assertEqual(name_6_clean, name_6_expected)

    def test_convert_to_url_name(self):
        #ARRANGE
        name_1_raw = u'Leslie Lewis (3)'
        name_1_expected = 'leslie-lewis'

        name_2_raw = 'Leslie Lewis (3)'
        name_2_expected = 'leslie-lewis'

        name_3_raw = u' lulu   ekiert '
        name_3_expected = u'lulu-ekiert'

        name_4_raw = u'Aimee McCabe - Karr'
        name_4_expected = u'aimee-mccabe-karr'

        #ACT
        name_1_clean = Instructor.convert_to_url_name(name_1_raw)
        name_2_clean = Instructor.convert_to_url_name(name_2_raw)
        name_3_clean = Instructor.convert_to_url_name(name_3_raw)
        name_4_clean = Instructor.convert_to_url_name(name_4_raw)

        #ASSERT
        self.assertEqual(name_1_clean, name_1_expected)
        self.assertEqual(name_2_clean, name_2_expected)
        self.assertEqual(name_3_clean, name_3_expected)
        self.assertEqual(name_4_clean, name_4_expected)

    #TODO: post on StackOvefflow how to set up Django tests to auto-discover all its tests in project/application
    #TODO: Understand difference between Mock Patterns: 'action -> assertion' vs 'record -> replay' (http://docs.python.org/dev/library/unittest.mock)


    @patch('schyoga.models.Instructor')
    def test_find_by_alias_one_instructor(self, instructor_1):
        #ARRANGE
        instructor_1.aliases_list = list(['Aimee McCabe - Karr'])
        studio_instructors = list([instructor_1])

        #ACT
        instructors = Instructor.find_by_alias(studio_instructors, 'Aimee McCabe - Karr')

        #ASSERT
        self.assertIsNotNone(instructors)
        self.assertEqual(len(instructors), 1)
        self.assertEqual(instructors[0], instructor_1)


    @patch('schyoga.models.Instructor')
    def test_find_by_alias_found_no_instructor(self, instructor_1):
        #ARRANGE
        instructor_1.aliases_list = list(['Aimee McCabe - Karr'])
        studio_instructors = list([instructor_1])

        #ACT
        instructors = Instructor.find_by_alias(studio_instructors, 'Idont exist')

        #ASSERT
        self.assertIsNone(instructors)


    @patch('schyoga.models.Instructor')
    @patch('schyoga.models.Instructor')
    def test_find_by_alias_two_instructors(self, instructor_1, instructor_2):
        #ARRANGE
        instructor_1.aliases_list = list(['Aimee McCabe - Karr'])
        instructor_2.aliases_list = list(['Nadya Zalota'])

        studio_instructors = list([instructor_1, instructor_2])

        #ACT
        instructors = Instructor.find_by_alias(studio_instructors, 'Nadya Zalota')

        #ASSERT
        self.assertIsNotNone(instructors)
        self.assertEqual(len(instructors), 1)
        self.assertEqual(instructors[0], instructor_2)


    @patch('schyoga.models.Instructor')
    @patch('schyoga.models.Instructor')
    def test_find_by_alias_two_instructors_same_alias(self, instructor_1, instructor_2):
        #ARRANGE
        instructor_1.aliases_list = ['Aimee McCabe - Karr', 'Teacher_1']
        instructor_2.aliases_list = ['Nadya Zalota', 'Instructor_1', 'Teacher_1', 'Yogi_1' ]

        studio_instructors = list([instructor_1, instructor_2])

        #ACT
        instructors = Instructor.find_by_alias(studio_instructors, 'Teacher_1')

        #ASSERT
        self.assertIsNotNone(instructors)
        self.assertEqual(len(instructors), 2)
        self.assertIn(instructor_1,instructors)
        self.assertIn(instructor_2,instructors)
        #self.assertEqual(instructors[0], instructor_2)