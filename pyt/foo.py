import numpy as np
import ctypes

lib = ctypes.CDLL("./ceditmat.so")
cf = lib.cfun
cf.restype = None
cf.argtypes = [np.ctypeslib.ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
               ctypes.c_size_t,
               np.ctypeslib.ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]


def f(m: np.matrix) -> None:
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            m[i, j] = i*m.shape[1] + j


m = np.zeros((2, 3))
f(m)
print(m)

indata = np.zeros((2, 3))
outdata = np.empty((2, 3))
cf(indata, indata.size, outdata)

print(outdata)

n = np.array([1, 2, 0, 1])

pi = np.zeros((2, 1))
pi[1, 0] = 1
t = np.zeros((2, 2))
e = np.zeros((2, 2))
v = np.zeros((pi.size, n.size))

print(n, pi, t, e, v)
