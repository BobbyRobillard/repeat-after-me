from utils import set_current_profile, get_current_profile

import unittest


class UtilsTestCase(unittest.TestCase):

    def test_set_current_profile(self):

        set_current_profile(2)

        self.assertEqual(get_current_profile("test")[0], 2)


if __name__ == '__main__':
    unittest.main()
