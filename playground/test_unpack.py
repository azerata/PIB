import numpy as np
from ctypes import CDLL, c_double, c_int

lib = CDLL('./unpack.so')
unpack = lib.unpack

unpack.restype = None
unpack.argtypes = [np.ctypeslib.ndpointer(
    c_double), np.ctypeslib.ndpointer(c_int), c_int]

trans = np.array([[0.10, 0.90, 0, 0, 0, 0, 0],
                  [0, 0.10, 0.90, 0, 0, 0, 0],
                  [0, 0, 0.10, 0.90, 0, 0, 0],
                  [0.20, 0, 0, 0.10, 0.70, 0, 0],
                  [0, 0, 0, 0, 0.10, 0.90, 0],
                  [0, 0, 0, 0, 0, 0.10, 0.90],
                  [0, 0, 0, 0.90, 0, 0, 0.10]], dtype=c_double)

outarr = np.zeros((1, 30), dtype=c_int)
unpack(trans, outarr, c_int(7))
