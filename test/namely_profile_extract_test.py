import namely_profile_extract
import unittest


class NamelyTest(unittest.TestCase):
    def test_normalise_1(self):
        before = "hello"
        after = namely_profile_extract.normalise(before)
        self.assertEqual(before, after)

    def test_normalise_2(self):
        before = "hello,world"
        after = namely_profile_extract.normalise(before)
        self.assertEqual('"{}"'.format(before), after)

    def test_normalise_3(self):
        before = 'this"is a "test'
        after = namely_profile_extract.normalise(before)
        self.assertEqual(before, after)

    def test_normalise_4(self):
        before = 'this is ", a test"'
        after = namely_profile_extract.normalise(before)
        self.assertEqual('"this is "", a test"""', after)


if __name__ == "__main__":
    unittest.main()
