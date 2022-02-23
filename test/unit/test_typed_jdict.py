import json
from typing import Final, Optional
from unittest import TestCase, main

from jdict import jdict, set_codec


class Point2D(jdict):
    x: Final[int]
    y: int
    label: Optional[str]


class TestTypedJdict(TestCase):
    def setUp(self):
        set_codec(json)

    def _validate_point(self, p) -> None:
        self.assertEqual(10, p.x)
        if issubclass(int, type(p.y)):
            self.assertEqual(25, p.y)
        else:
            self.assertNotEqual(25, p.y)
        if hasattr(p, "label"):
            self.assertEqual("first point", p.label)

    def test_normal_initialization(self):
        self._validate_point(Point2D(x=10, y=25, label="first point"))

    def test_no_optional_initialization(self):
        self._validate_point(Point2D(x=10, y=25))

    def test_wrong_type(self):
        p = Point2D(x=10, y="25", label="first point")  # PyCharm will not complain :-(
        self._validate_point(p)

    def test_missing_argument(self):
        self.assertRaises(
            TypeError, Point2D, x=10, label="first point"
        )  # PyCharm will not complain, but it fails in run-time

    def test_update_existing(self):
        p = Point2D(x=10, y=25, label="first point")
        p.y = 45
        self.assertEqual(45, p.y)

    def test_update_optional(self):
        p = Point2D(x=10, y=25)
        p.label = "missing label"
        self.assertEqual("missing label", p.label)

    def test_update_final(self):
        p = Point2D(x=10, y=25, label="first point")
        with self.assertRaises(AttributeError) as ae:
            p.x = 45  # PyCharm complains and it fill fail

    def test_set_non_existent(self):
        p = Point2D(x=10, y=25, label="first point")
        with self.assertRaises(AttributeError) as ae:
            p.z = 45  # PyCharm does not complain but it fill fail


if __name__ == "__main__":
    main()
