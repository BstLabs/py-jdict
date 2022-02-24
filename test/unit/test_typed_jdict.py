import json
from typing import Final, Optional
from unittest import TestCase, main

from jdict import jdict, set_codec


class Point2D(jdict):
    x: Final[int]
    y: int
    label: Optional[str]


class TestTypedJdict(TestCase):
    @classmethod
    def setUpClass(cls):
        set_codec(json)
        cls.point = Point2D(x=10, y=25, label="first point")

    def _validate_point(self, p) -> None:
        self.assertEqual(10, p.x)
        if issubclass(int, type(p.y)):
            self.assertEqual(25, p.y)
        else:
            self.assertNotEqual(25, p.y)
        if hasattr(p, "label"):
            self.assertEqual("first point", p.label)

    def test_normal_initialization(self):
        self._validate_point(self.point)

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
        self.point.y = 45
        self.assertEqual(45, self.point.y)

    def test_update_optional(self):
        p = Point2D(x=10, y=25)
        p.label = "missing label"
        self.assertEqual("missing label", p.label)

    def test_update_final(self):
        self.point.x = 45  # static type checkers and linters will complain about Final
        self.assertEqual(45, self.point.x)

    def test_set_non_existent(self):
        self.point.z = 45
        self.assertEqual(45, self.point.z)


if __name__ == "__main__":
    main()
