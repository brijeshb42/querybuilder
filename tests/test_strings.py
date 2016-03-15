import unittest
from querybuilder.helpers import AND, OR, Field as F


class QbTest(unittest.TestCase):

    def test_basics(self):
        q1 = F('pageviews') == 1
        q2 = F('pageviews').eq(1)
        res = {"EQ": {"pageviews": 1}}
        self.assertEqual(cmp(q1, res), 0)
        self.assertEqual(cmp(q2, res), 0)
        self.assertEqual(cmp(q1, q2), 0)

        q1 = F('pageviews') != 1
        q2 = F('pageviews').ne(1)
        res = {"NE": {"pageviews": 1}}
        self.assertEqual(cmp(q1, res), 0)
        self.assertEqual(cmp(q2, res), 0)
        self.assertEqual(cmp(q1, q2), 0)

        q1 = F('pageviews') >= 1
        q2 = F('pageviews').ge(1)
        res = {"GE": {"pageviews": 1}}
        self.assertEqual(cmp(q1, res), 0)
        self.assertEqual(cmp(q2, res), 0)
        self.assertEqual(cmp(q1, q2), 0)

        q1 = F('pageviews') > 1
        q2 = F('pageviews').gt(1)
        res = {"GT": {"pageviews": 1}}
        self.assertEqual(cmp(q1, res), 0)
        self.assertEqual(cmp(q2, res), 0)
        self.assertEqual(cmp(q1, q2), 0)

        q1 = F('pageviews') < 1
        q2 = F('pageviews').lt(1)
        res = {"LT": {"pageviews": 1}}
        self.assertEqual(cmp(q1, res), 0)
        self.assertEqual(cmp(q2, res), 0)
        self.assertEqual(cmp(q1, q2), 0)

        q1 = F('pageviews') <= 1
        q2 = F('pageviews').le(1)
        res = {"LE": {"pageviews": 1}}
        self.assertEqual(cmp(q1, res), 0)
        self.assertEqual(cmp(q2, res), 0)
        self.assertEqual(cmp(q1, q2), 0)

        q1 = F('pageviews') << (1, 2, 3)
        q2 = F('pageviews').in_(1, 2, 3)
        res = {"IN": {"pageviews": (1, 2, 3)}}
        self.assertEqual(cmp(q1, res), 0)
        self.assertEqual(cmp(q2, res), 0)
        self.assertEqual(cmp(q1, q2), 0)

        q1 = F('pageviews').contains(1, 2, 3)
        res = {"CONTAINS": {"pageviews": (1, 2, 3)}}
        self.assertEqual(cmp(q1, res), 0)

        q1 = F('pageviews').contains_any(1, 2, 3)
        res = {"CONTAINS_ANY": {"pageviews": (1, 2, 3)}}
        self.assertEqual(cmp(q1, res), 0)

        q1 = F('pageviews').contains_all(1, 2, 3)
        res = {"CONTAINS_ALL": {"pageviews": (1, 2, 3)}}
        self.assertEqual(cmp(q1, res), 0)

        q1 = F('pageviews').between(1, 2)
        res = {"BETWEEN": {"pageviews": (1, 2)}}
        self.assertEqual(cmp(q1, res), 0)

        q1 = F('published').between("2016-03-07", "2016-03-08")
        res = {"BETWEEN": {"published": ("2016-03-07", "2016-03-08")}}
        self.assertEqual(cmp(q1, res), 0)

        self.assertRaises(ValueError, F('pageviews').eq, 1, 2)
        self.assertRaises(ValueError, F('pageviews').ne, 1, 2)
        self.assertRaises(ValueError, F('pageviews').gt, 1, 2)
        self.assertRaises(ValueError, F('pageviews').ge, 1, 2)
        self.assertRaises(ValueError, F('pageviews').lt, 1, 2)
        self.assertRaises(ValueError, F('pageviews').le, 1, 2)

    def test_more(self):
        q1 = AND(F("pageviews") >= 100, F("series_id") == 1)
        res = {"AND": ({"GE": {"pageviews": 100}}, {"EQ": {"series_id": 1}})}
        self.assertEqual(cmp(q1, res), 0)

        q1 = OR(
            AND(F("pageviews") >= 100, F("series_id") == 1),
            AND(F("pageviews") <= 1000, F("series_id") != 0)
        )
        res = {"OR": ({"AND": ({"GE": {"pageviews": 100}}, {"EQ": {"series_id": 1}})},
                {"AND": ({"LE": {"pageviews": 1000}}, {"NE": {"series_id": 0}})})}
        self.assertEqual(cmp(q1, res), 0)
