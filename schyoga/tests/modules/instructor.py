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

        name_7_raw = u" TEACHER "
        name_7_expected = u''

        name_8_raw = u" Teacher   TEACHER  "# bikram yoga harlem
        name_8_expected = u''

        name_9_raw = u"  Staff  "
        name_9_expected = u''

        name_10_raw = u"  Staff   staff  "
        name_10_expected = u''

        name_11_raw = u"  STAFF   MEMBER  " # Atmananda Yoga Sequence
        name_11_expected = u''

        name_12_raw = u"    GOLDEN  BRIDGE   STAFF "
        #name_12_raw = u" Lotus STAFF "
        name_12_expected = u''

        name_13_raw = u"  STAFF  "
        name_13_expected = u''

        #ACT
        name_1_clean = Instructor.clean_up_name(name_1_raw)
        name_2_clean = Instructor.clean_up_name(name_2_raw)
        name_3_clean = Instructor.clean_up_name(name_3_raw)
        name_4_clean = Instructor.clean_up_name(name_4_raw)
        name_5_clean = Instructor.clean_up_name(name_5_raw)
        name_6_clean = Instructor.clean_up_name(name_6_raw)
        name_7_clean = Instructor.clean_up_name(name_7_raw)
        name_8_clean = Instructor.clean_up_name(name_8_raw)
        name_9_clean = Instructor.clean_up_name(name_9_raw)
        name_10_clean = Instructor.clean_up_name(name_10_raw)
        name_11_clean = Instructor.clean_up_name(name_11_raw)
        name_12_clean = Instructor.clean_up_name(name_12_raw)
        name_13_clean = Instructor.clean_up_name(name_13_raw)

        #ASSERT
        self.assertEqual(name_1_clean, name_1_expected)
        self.assertEqual(name_2_clean, name_2_expected)
        self.assertEqual(name_3_clean, name_3_expected)
        self.assertEqual(name_4_clean, name_4_expected)
        self.assertEqual(name_5_clean, name_5_expected)
        self.assertEqual(name_6_clean, name_6_expected)
        self.assertEqual(name_7_clean, name_7_expected)
        self.assertEqual(name_8_clean, name_8_expected)
        self.assertEqual(name_9_clean, name_9_expected)
        self.assertEqual(name_10_clean, name_10_expected)
        self.assertEqual(name_11_clean, name_11_expected)
        self.assertEqual(name_12_clean, name_12_expected)
        self.assertEqual(name_13_clean, name_13_expected)

    def test_clean_up_name2(self):
        #ARRANGE
        name_1_raw = u"  Karina   Hluhovs'ka  "# teacher from Go Yoga studio
        name_1_expected = u'Karina Hluhovska'

        name_2_raw = '  Jennifer A. '
        name_2_expected = 'Jennifer A'

        name_3_raw = u'Grace (Sangeet Kaur) Kim (12)'
        name_3_expected = u'Grace (Sangeet Kaur) Kim'

        name_4_raw = u" Ambyr D'Amato " # Loom Studios
        name_4_expected = u'Ambyr DAmato'

        name_5_raw = u"  TBA . "
        name_5_expected = u''

        name_6_raw = u"  Blossoming Teachers "
        name_6_expected = u''

        name_7_raw = u" * * "
        name_7_expected = u''

        name_8_raw = u" YTTP "
        name_8_expected = u''

        name_9_raw = u"    "
        name_9_expected = u''

        name_10_raw = u" "
        name_10_expected = u''

        #ACT
        name_1_clean = Instructor.clean_up_name(name_1_raw)
        name_2_clean = Instructor.clean_up_name(name_2_raw)
        name_3_clean = Instructor.clean_up_name(name_3_raw)
        name_4_clean = Instructor.clean_up_name(name_4_raw)
        name_5_clean = Instructor.clean_up_name(name_5_raw)
        name_6_clean = Instructor.clean_up_name(name_6_raw)
        name_7_clean = Instructor.clean_up_name(name_7_raw)
        name_8_clean = Instructor.clean_up_name(name_8_raw)
        name_9_clean = Instructor.clean_up_name(name_9_raw)
        name_10_clean = Instructor.clean_up_name(name_10_raw)

        #ASSERT
        self.assertEqual(name_1_clean, name_1_expected)
        self.assertEqual(name_2_clean, name_2_expected)
        self.assertEqual(name_3_clean, name_3_expected)
        self.assertEqual(name_4_clean, name_4_expected)
        self.assertEqual(name_5_clean, name_5_expected)
        self.assertEqual(name_6_clean, name_6_expected)
        self.assertEqual(name_7_clean, name_7_expected)
        self.assertEqual(name_8_clean, name_8_expected)
        self.assertEqual(name_9_clean, name_9_expected)
        self.assertEqual(name_10_clean, name_10_expected)


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