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

num_rows = a.shape[0]
num_cols = a.shape[1]

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
    ffi.cdef(my_header.read().replace('NUM_COLS', str(num_cols)))  # IMPORTANT! cffi limitation

with open('test.c') as my_source:
    if __debug__:
        print('Building the debug build...')
        ffi.set_source(
            '_test',
            my_source.read(),
            extra_compile_args=['-fopenmp', '-Wall', '-g', '-O0']
        )
    else:
        if use_openmp:
            print('Building for performance with OpenMP...')
            ffi.set_source(
                '_test',
                my_source.read(),
                extra_compile_args=['-fopenmp', '-D use_openmp', '-Ofast'],
                extra_link_args=['-fopenmp'],
            )
        else:
            print('Building for performance without OpenMP...')
            ffi.set_source('_test', my_source.read(), extra_compile_args=['-Ofast'])

ffi.compile()  # convert and compile - mandatory!

import _test

assert (_test.lib.myadder(10,12)) - (10+12) < 0.01  # A - B < 0.1 if A ~= B

_test.lib.add_array(
    _test.ffi.cast('int', num_rows),
    _test.ffi.cast('int', num_cols),
    _test.ffi.cast('double (*)[3]', a.__array_interface__['data'][0]),
    _test.ffi.cast('double (*)[3]', b.__array_interface__['data'][0]),
    _test.ffi.cast('double (*)[3]', result.__array_interface__['data'][0]),
)

assert numpy.array_equal(a+b, result)
print('All OK!')
