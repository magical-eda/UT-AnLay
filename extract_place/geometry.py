##
# @file geometry.py
# @author Keren Zhu
# @date May 2019
# @brief Data structure for basic geometry
#

import sys

class XY(object):
    def __init__(self, x = -1,y = -1):
        self._x = x
        self._y = y
    def set_x(self, x):
        self._x = x
    def set_y(self, y):
        self._y = y
    def x(self):
        return self._x
    def y(self):
        return self._y
    def to_str(self):
        string = ""
        string += "( " + str(self._x) + " , " + str(self._y) + " )"
        return string

class Rect(object):
    def __init__(self, x_lo = sys.maxint, y_lo = sys.maxint, x_hi = -sys.maxint - 1, y_hi = -sys.maxint - 1):
        self._ll = XY(x_lo, y_lo)
        self._ur = XY(x_hi, y_hi)
    def x_lo(self):
        return self._ll.x()
    def set_x_lo(self, x_lo):
        self._ll.set_x(x_lo)
    def y_lo(self):
        return self._ll.y()
    def set_y_lo(self, y_lo):
        self._ll.set_y(y_lo)
    def x_hi(self):
        return self._ur.x()
    def set_x_hi(self, x_hi):
        self._ur.set_x(x_hi)
    def y_hi(self):
        return self._ur.y()
    def set_y_hi(self, y_hi):
        self._ur.set_y(y_hi)
    def ll(self):
        return self._ll
    def set_ll(self, ll):
        self._ll = ll
    def ur(self):
        return self._ur
    def set_ur(self, ur):
        self._ur = ur
    def width(self):
        return self._ur.x() - self._ll.x()
    def height(self):
        return self._ur.y() - self._ll.y()
    def join(self, xy):
        """
        @brief extend the rectangle to cover the given point
        @param a point
        """
        self._ll.set_x(min(self._ll.x(), xy.x()))
        self._ll.set_y(min(self._ll.y(), xy.y()))
        self._ur.set_x(max(self._ur.x(), xy.x()))
        self._ur.set_y(max(self._ur.y(), xy.y()))
    def union(self, rhs):
        """
        @brief Extend the rectangle to cover another rectangle
        @param a Rect
        """
        self.join(rhs.ll())
        self.join(rhs.ur())
    def offset_by(self, offset_x, offset_y):
        self._ll.set_x(self._ll.x() + offset_x)
        self._ll.set_y(self._ll.y() + offset_y)
        self._ur.set_x(self._ur.x() + offset_x)
        self._ur.set_y(self._ur.y() + offset_y)
    def to_str(self):
        string = ""
        string += self._ll.to_str() + "->" +  self._ur.to_str()
        return string
