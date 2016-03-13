import unittest
from querybuilder import AND, OR, Field as F


class QbTest(unittest.TestCase):

    def test_basics(self):
        q1 = F('pageviews') == 1
        q2 = F('pageviews').eq(1)
        self.assertEqual(q1, 'EQ("pageviews", 1)')
        self.assertEqual(q1, q2)

        q1 = F('pageviews') != 1
        q2 = F('pageviews').ne(1)
        self.assertEqual(q1, 'NE("pageviews", 1)')
        self.assertEqual(q1, q2)

        q1 = F('pageviews') >= 1
        q2 = F('pageviews').ge(1)
        self.assertEqual(q1, 'GE("pageviews", 1)')
        self.assertEqual(q1, q2)

        q1 = F('pageviews') > 1
        q2 = F('pageviews').gt(1)
        self.assertEqual(q1, 'GT("pageviews", 1)')
        self.assertEqual(q1, q2)

        q1 = F('pageviews') < 1
        q2 = F('pageviews').lt(1)
        self.assertEqual(q1, 'LT("pageviews", 1)')
        self.assertEqual(q1, q2)

        q1 = F('pageviews') <= 1
        q2 = F('pageviews').le(1)
        self.assertEqual(q1, 'LE("pageviews", 1)')
        self.assertEqual(q1, q2)

        q1 = F('pageviews') << (1, 2, 3)
        q2 = F('pageviews').in_(1, 2, 3)
        self.assertEqual(q1, 'IN("pageviews", 1, 2, 3)')
        self.assertEqual(q1, q2)

        q1 = F('pageviews').contains(1, 2, 3)
        self.assertEqual(q1, 'CONTAINS("pageviews", 1, 2, 3)')

        q1 = F('pageviews').contains_any(1, 2, 3)
        self.assertEqual(q1, 'CONTAINS_ANY("pageviews", 1, 2, 3)')

        q1 = F('pageviews').contains_all(1, 2, 3)
        self.assertEqual(q1, 'CONTAINS_ALL("pageviews", 1, 2, 3)')

        q1 = F('pageviews').between(1, 2)
        self.assertEqual(q1, 'BETWEEN("pageviews", 1, 2)')

        self.assertRaises(ValueError, F('pageviews').eq, 1, 2)
        self.assertRaises(ValueError, F('pageviews').ne, 1, 2)
        self.assertRaises(ValueError, F('pageviews').gt, 1, 2)
        self.assertRaises(ValueError, F('pageviews').ge, 1, 2)
        self.assertRaises(ValueError, F('pageviews').lt, 1, 2)
        self.assertRaises(ValueError, F('pageviews').le, 1, 2)

        self.assertRaises(ValueError, F('pageviews').between, 1)
        self.assertRaises(ValueError, F('pageviews').between, 1, 2, 3)
