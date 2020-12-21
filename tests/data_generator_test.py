import unittest
from uuid import UUID

from testgen import DataGenerator
from testgen.exceptions import DataGenerationException

FILE_NAME = 'file'


class DataGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.generator = DataGenerator()

    def test_prefix_func_count(self):
        count_func = self.generator.create_filename_func(FILE_NAME, 'count')
        self.check_prefixes(count_func)

    def test_prefix_func_random(self):
        random_func = self.generator.create_filename_func(FILE_NAME, 'random')
        self.check_prefixes(random_func)

    def test_prefix_func_uuid(self):
        uuid_func = self.generator.create_filename_func(FILE_NAME, 'uuid')
        self.check_prefixes(uuid_func)
        uuid_str = uuid_func().split('_')[1]
        self.assertTrue(self.is_valid_uuid(uuid_str))

    def test_prefix_wrong_argument(self):
        try:
            self.generator.create_filename_func(FILE_NAME, 'wrong_arg')
        except DataGenerationException as e:
                self.assertEqual(str(e), 'file_prefix has wrong value'
                                         '')

    def check_prefixes(self, func):
        filename_1 = func()
        filename_2 = func()
        filename_3 = func()
        self.assertTrue(str(filename_1).startswith(FILE_NAME))
        self.assertTrue(str(filename_2).startswith(FILE_NAME))
        self.assertTrue(str(filename_3).startswith(FILE_NAME))
        pref_1 = filename_1.split('_')[1]
        pref_2 = filename_2.split('_')[1]
        pref_3 = filename_3.split('_')[1]
        self.assertTrue(pref_1 != pref_2 and pref_2 != pref_3 and pref_3 != pref_1)

    def is_valid_uuid(self, uuid_to_test, version=4):
        try:
            uuid_obj = UUID(uuid_to_test, version=version)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test


if __name__ == '__main__':
    unittest.main()
