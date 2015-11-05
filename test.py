import sys
use_openmp = False
try:
    if sys.argv[1] == 'use_openmp':
        use_openmp = True
except IndexError:
    pass

import cffi
ffi = cffi.FFI()

with open('test.h') as my_header:
    ffi.cdef(my_header.read())
with open('test.c') as my_source:
    if __debug__:
        ffi.set_source(
            '_test',
            my_source.read(),
            extra_compile_args=['-fopenmp', '-Wall', '-g', '-O0']
        )
    else:
        if use_openmp:
            ffi.set_source(
                '_test',
                my_source.read(),
                extra_compile_args=['-D use_openmp', '-fopenmp', '-Ofast']
            )
        else:
            ffi.set_source('_test', my_source.read(), extra_compile_args=['-Ofast'])

ffi.compile()  # convert and compile - mandatory!

import _test
assert (_test.lib.myadder(10,12)) - (10+12) < 0.01  # A - B < 0.1 if A ~= B

import numpy
a = numpy.array(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ], dtype=numpy.float64
)

b = numpy.array(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ], dtype=numpy.float64
)

result = numpy.zeros_like(a)

_test.lib.add_array(
    _test.ffi.cast('int', a.shape[0]),
    _test.ffi.cast('int', a.shape[1]),
    _test.ffi.cast('double (*)[3]', a.__array_interface__['data'][0]),
    _test.ffi.cast('double (*)[3]', b.__array_interface__['data'][0]),
    _test.ffi.cast('double (*)[3]', result.__array_interface__['data'][0]),
)

assert numpy.array_equal(a+b, result)
