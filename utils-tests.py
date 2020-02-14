from utils import (set_current_profile, get_current_profile, set_recording_key,
                   get_recording_key, set_active_mode_key, get_active_mode_key,
                   set_play_mode_key, get_play_mode_key, add_profile,
                   get_profiles, is_recording, start_recording, stop_recording)

import unittest
import utils


class UtilsTestCase(unittest.TestCase):

    def test_add_profile(self):
        original_count = len(get_profiles())
        add_profile("test1")
        add_profile("test2")
        add_profile("test3")
        self.assertEqual(len(get_profiles()), original_count + 3)

    def test_set_current_profile(self):
        set_current_profile(2)
        self.assertEqual(get_current_profile("test")[0], 2)

    def test_set_recording_key(self):
        set_recording_key("25")
        self.assertEqual(get_recording_key(), "25")

    def test_set_active_mode_key(self):
        set_active_mode_key("a")
        self.assertEqual(get_active_mode_key(), "a")

    def test_set_play_mode_key(self):
        set_play_mode_key("c")
        self.assertEqual(get_play_mode_key(), "c")

    def test_start_recording(self):
        start_recording()
        self.assertEqual(utils.is_recording, True)

    def test_stop_recording(self):
        stop_recording()
        self.assertEqual(utils.is_recording, False)


if __name__ == '__main__':
    unittest.main()
