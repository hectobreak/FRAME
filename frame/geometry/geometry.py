"""
Module to represent points, shapes and rectangles
"""
from __future__ import annotations
from typing import NamedTuple, Tuple, Any

from ..utils.keywords import KW_FIXED, KW_CENTER, KW_SHAPE, KW_REGION, KW_NAME, KW_GROUND
from ..utils.utils import valid_identifier


class Point:
    """
    A class to represent a two-dimensional point, and operate with them
    """
    def __init__(self, x: Point | tuple[float, float] | float | None = None, y: float | None = None) -> None:
        """
        Constructor of a Point. See the example for ways of constructing it.

        :param x: a Point or tuple[float, float], a float, or None.
        :param y: None if x is a Point, tuple[float, float] or None, or a float if x is a float.

        :Example:
        >>> Point()
        Point(x=0, y=0)
        >>> Point(1)
        Point(x=1, y=1)
        >>> Point(1, 2)
        Point(x=1, y=2)
        >>> Point((1, 2))
        Point(x=1, y=2)
        """
        if x is None:  # x and y are None
            self.x, self.y = 0, 0
        elif y is None:  # x is a Point or a number and y is None
            if isinstance(x, Point):
                self.x, self.y = x.x, x.y
            elif isinstance(x, tuple):
                self.x, self.y = x
            else:
                self.x, self.y = x, x
        else:  # x and y are numbers
            self.x, self.y = x, y

    def __eq__(self, other: Point) -> bool:
        """Return self == other."""
        return self.x == other.x and self.y == other.y

    def __neg__(self) -> Point:
        """Return -self."""
        return Point(-self.x, -self.y)

    def __add__(self, other: float | Point) -> Point:
        """Return self + other."""
        other = Point(other)
        return Point(self.x + other.x, self.y + other.y)

    __radd__ = __add__

    def __sub__(self, other: float | Point) -> Point:
        """Return self - other."""
        other = Point(other)
        return Point(self.x, self.y) + -other

    def __rsub__(self, other: float | Point) -> Point:
        """Return other - self."""
        other = Point(other)
        return other - self

    def __mul__(self, other: float | Point) -> Point:
        """Return self*other using component-wise multiplication. other can either be a number or another point."""
        other = Point(other)
        return Point(self.x*other.x, self.y*other.y)

    __rmul__ = __mul__

    def __pow__(self, exponent: float) -> Point:
        """Return self**exponent using component-wise exponentiation."""
        return Point(self.x**exponent, self.y**exponent)

    def __truediv__(self, other: float | Point) -> Point:
        """Return self / other using component-wise true division. other can either be a number or another point."""
        other = Point(other)
        return Point(self.x/other.x, self.y/other.y)

    def __rtruediv__(self, other: float | Point):
        """Return other / self using component-wise true division. other can either be a number or another point."""
        other = Point(other)
        return Point(other.x/self.x, other.y/self.y)

    def __and__(self, other: Point) -> float:
        """Dot product between self and other."""
        return self.x*other.x + self.y*other.y

    def __str__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    __repr__ = __str__

    def __iter__(self):
        yield self.x
        yield self.y


class Shape(NamedTuple):
    """
    A class to represent a two-dimensional rectilinear shape (width and height)
    """
    w: float
    h: float


class Rectangle:
    """
    A class to represent a rectilinear rectangle
    """

    def __init__(self, **kwargs: Any):
        """
        Constructor
        :param kwargs: center (Point), shape (Shape), fixed (bool), region (str)
        """

        # Attributes
        self._center: Point = Point(-1, -1)     # Center of the rectangle
        self._shape: Shape = Shape(-1, -1)      # Shape: width and height
        self._fixed: bool = False               # Is the rectangle fixed?
        self._region: str = KW_GROUND           # Region of the layout to which the rectangle belongs to
        self._name: str = ""                    # Name of the rectangle

        # Reading parameters and type checking
        for key, value in kwargs.items():
            assert key in [KW_CENTER, KW_SHAPE, KW_FIXED, KW_REGION, KW_NAME], "Unknown rectangle attribute"
            if key == KW_CENTER:
                assert isinstance(value, Point), "Incorrect point associated to the center of the rectangle"
                self._center = value
            elif key == KW_SHAPE:
                assert isinstance(value, Shape), "Incorrect shape associated to the rectangle"
                assert value.w > 0, "Incorrect rectangle width"
                assert value.h > 0, "Incorrect rectangle height"
                self._shape = value
            elif key == KW_FIXED:
                assert isinstance(value, bool), "Incorrect value for fixed (should be a boolean)"
                self._fixed = value
            elif key == KW_REGION:
                assert valid_identifier(value), \
                    "Incorrect value for region (should be a valid string)"
                self._region = value
            elif key == KW_NAME:
                assert isinstance(value, str), "Incorrect value for rectangle"
                self._name = value
            else:
                assert False  # Should never happen

    # Getter and setter for center
    @property
    def center(self) -> Point:
        return self._center

    @center.setter
    def center(self, p: Point) -> None:
        self._center = p

    # Getter and setter for shape
    @property
    def shape(self) -> Shape:
        return self._shape

    @shape.setter
    def shape(self, shape) -> None:
        self._shape = shape

    @property
    def bounding_box(self) -> Tuple[Point, Point]:
        """
        :return: a tuple ((xmin, ymin), (xmax, ymax))
        """
        half_w, half_h = self.shape.w / 2, self.shape.h / 2
        xmin, xmax = self.center.x - half_w, self.center.x + half_w
        ymin, ymax = self.center.y - half_h, self.center.y + half_h
        return Point(xmin, ymin), Point(xmax, ymax)

    @property
    def area(self) -> float:
        return self._shape.w * self._shape.h

    @property
    def fixed(self) -> bool:
        return self._fixed

    @property
    def region(self) -> str:
        return self._region

    @region.setter
    def region(self, region: str) -> None:
        self._region = region

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name) -> None:
        self._name = name

    def inside(self, p: Point) -> bool:
        """
        Checks whether a point is inside the rectangle
        :param p: the point
        :return: True if inside, False otherwise
        """
        bb = self.bounding_box
        return bb[0].x <= p.x <= bb[1].x and bb[0].y <= p.y <= bb[1].y

    def overlap(self, r: Rectangle) -> bool:
        """
        Checks whether two rectangles overlap. They are considered not to overlap if they touch each other
        :param r: the other rectangle.
        :return: True if they overlap, and False otherwise.
        """
        ll1, ur1 = self.bounding_box
        ll2, ur2 = r.bounding_box
        if ur1.x <= ll2.x or ur2.x <= ll1.x:
            return False
        return ur1.y > ll2.y and ur2.y > ll1.y

    def __str__(self) -> str:
        """
        :return: string representation of the rectangle
        """
        s = f"{KW_CENTER}={self.center} {KW_SHAPE}={self.shape} {KW_REGION}={self.region}"
        if self.fixed:
            s += f" {KW_FIXED}"
        return s

    __repr__ = __str__
