import unittest

from trino_bouncer.bouncer import Bouncer


class BouncerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.bouncer = Bouncer()
        self.bouncer.add_targets({
            "green": "http://green.local",
            "blue": "http://blue.local",
        })

    def test_add_target(self):
        self.bouncer.add_target("black", "http://black.local")

    def test_add_invalid_target(self):
        with self.assertRaises(ValueError):
            self.bouncer.add_target("black", "not a url")

    def test_add_existing_target(self):
        with self.assertRaises(ValueError):
            self.bouncer.add_target("green", "doesn't matter")

    def test_update_target(self):
        self.bouncer.update_target("green", "http://green2.local")

    def test_update_invalid_target(self):
        with self.assertRaises(ValueError):
            self.bouncer.update_target("green", "not a target")

    def test_update_multi_target(self):
        self.bouncer.update_targets({
            "green": "http://green2.local",
            "blue": "http://blue2.local",
        })
        self.assertIn("green2", self.bouncer.targets["green"])
        self.assertIn("blue2", self.bouncer.targets["blue"])

    def test_active_no_targets(self):
        self.bouncer._targets = {}
        with self.assertRaises(RuntimeError):
            _ = self.bouncer.active

    def test_active_no_active(self):
        result = self.bouncer.active
        self.assertEqual(result, ("green", "http://green.local"))

    def test_set_active_missing(self):
        with self.assertRaises(KeyError):
            self.bouncer.active = "black"

    def test_active(self):
        self.bouncer.active = "green"
        self.assertEqual(("green", "http://green.local"), self.bouncer.active)


if __name__ == '__main__':
    unittest.main()
