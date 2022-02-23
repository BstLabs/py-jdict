import datetime
import json
from copy import deepcopy
from unittest import TestCase, main

from jdict import jdict, set_codec
from jdict.transformer import transform


class TestJdict(TestCase):
    def setUp(self):
        self.data = {
            "location": "DEF",
            "voyageId": "XYZ",
            "eventType": "UNLOAD",
            "completionTime": 1526897537633,
        }
        set_codec(json)
        self.jdict = jdict(self.data)

    def test_jdict(self):
        self.assertEqual(self.data["location"], self.jdict.location)

    def test_transformer(self):
        self.new_tree = transform(
            'self.data = {"location": "DEF", "voyageId": "XYZ", '
            '"eventType": "UNLOAD", "completionTime": 1526897537633,}'
            '\nself.assertEqual(self.data.location, "DEF")'
        )

        exec(compile(self.new_tree, "file", "exec"))

    def test_deepcopy(self):
        d = deepcopy(self.jdict)
        self.assertEqual(d, self.jdict)
        self.jdict.time = 12.25
        self.assertNotEqual(self.jdict, d)
        self.assertEqual(type(d), jdict)

    def test_datetime_serializer(self):
        print(
            json.dumps(jdict(timestamp=datetime.datetime(2020, 10, 26)), indent=2)
        )  # should not fail


if __name__ == "__main__":
    main()
