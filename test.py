import numpy

a = numpy.array(
    [
        [1, 2, 3, 4, 5, 6],
        [4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 5, 6],
        [4, 5, 6, 7, 8, 9],
    ], dtype=numpy.float64
)

b = numpy.array(
    [
        [4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 5, 6],
        [6, 5, 4, 3, 1, 2],
        [1, 2, 3, 4, 5, 6],
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

# _test.ffi.from_buffer(my_array) is a less verbose alternative to:
# my_array.__array_interface__['data'][0]

_x = _test.ffi.cast('int', num_rows)
_y = _test.ffi.cast('int', num_cols)
_a = _test.ffi.cast('double (*)[{}]'.format(num_cols), _test.ffi.from_buffer(a))
_b = _test.ffi.cast('double (*)[{}]'.format(num_cols), _test.ffi.from_buffer(b))
_result = _test.ffi.cast('double (*)[{}]'.format(num_cols), _test.ffi.from_buffer(result))

_test.lib.add_array(_x, _y, _a, _b, _result)

assert numpy.array_equal(numpy.add(a,b), result)
print('All OK!')
