import unittest

from geometry import Point, Shape, Rectangle


class TestGeometry(unittest.TestCase):

    def test_bad_rectangles(self):
        # Bad constructors
        self.assertRaises(AssertionError, Rectangle, unknown=Point(1, 1))
        self.assertRaises(AssertionError, Rectangle, center=Shape(1, 1))
        self.assertRaises(AssertionError, Rectangle, shape=Point(1, 1))

    def test_area_rectangles(self):
        r = Rectangle(center=Point(5, 3), shape=Shape(4, 2))
        self.assertEqual(r.area, 8)
        self.assertTrue(r.inside(Point(3.1, 2.5)))
        self.assertFalse(r.inside(Point(2.9, 2.1)))
        self.assertFalse(r.inside(Point(3.1, 1.9)))
        self.assertEqual(r.bounding_box, (Point(3, 2), Point(7, 4)))
        r.shape = Shape(3, 1)
        self.assertEqual(r.area, 3)
        self.assertEqual(r.bounding_box, (Point(3.5, 2.5), Point(6.5, 3.5)))
        r.center = Point(30, 40)
        self.assertEqual(r.area, 3)
        self.assertEqual(r.bounding_box, (Point(28.5, 39.5), Point(31.5, 40.5)))


if __name__ == '__main__':
    unittest.main()
