import sys
import os
import cffi
ffi = cffi.FFI()

with open('test.h') as my_header:
    ffi.cdef(my_header.read())

with open('test.c') as my_source:
    if __debug__:
        print('Building the debug build without OpenMP...')
        ffi.set_source(
            '_test',
            my_source.read(),
            extra_compile_args=['-Werror', '-pedantic', '-Wall', '-g', '-O0']
        )
    else:
        if os.environ.get('USE_OPENMP'):
            print('Building for performance with OpenMP...')
            ffi.set_source(
                '_test',
                my_source.read(),
                extra_compile_args=['-fopenmp', '-D USE_OPENMP', '-Ofast'],
                extra_link_args=['-fopenmp'],
            )
        else:
            print('Building for performance without OpenMP...')
            ffi.set_source('_test', my_source.read(), extra_compile_args=['-Ofast'])

ffi.compile()  # convert and compile - mandatory!

import _test
assert (_test.lib.myadder(10,12)) - (10+12) < 0.01  # A - B < 0.1 if A ~= B

import numpy

a = numpy.array(
    [
        [1, 2, 3, 4, 5, 6],
        [4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 5, 6],
        [4, 5, 6, 7, 8, 9],
    ], dtype=numpy.float32
)

b = numpy.array(
    [
        [4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 5, 6],
        [6, 5, 4, 3, 1, 2],
        [1, 2, 3, 4, 5, 6],
    ], dtype=numpy.float32
)

result = numpy.zeros_like(a)

# equivalent (in theory):
# _test.ffi.from_buffer(my_array)
# my_array.__array_interface__['data'][0]
# my_array.ctypes.data

_x = _test.ffi.cast('size_t', a.shape[0])
_y = _test.ffi.cast('size_t', a.shape[1])
_a = _test.ffi.cast('float *', a.ctypes.data)
_b = _test.ffi.cast('float *', b.ctypes.data)
_result = _test.ffi.cast('float *', result.ctypes.data)

_test.lib.add_array_f(_x, _y, _a, _b, _result)
assert numpy.array_equal(numpy.add(a,b), result)
print('Test 1 OK!')

a = numpy.random.rand(10240, 10240).astype(numpy.float32)
b = numpy.random.rand(10240, 10240).astype(numpy.float32)
result = numpy.zeros_like(a)

_x = _test.ffi.cast('size_t', a.shape[0])
_y = _test.ffi.cast('size_t', a.shape[1])
_a = _test.ffi.cast('float *', a.ctypes.data)
_b = _test.ffi.cast('float *', b.ctypes.data)
_result = _test.ffi.cast('float *', result.ctypes.data)

_test.lib.add_array_f(_x, _y, _a, _b, _result)
assert numpy.array_equal(numpy.add(a,b), result)
print('Test 2 OK!')

import time
test_count = 5
start = time.clock()
for i in range(test_count):
    _test.lib.add_array_f(_x, _y, _a, _b, _result)
end = time.clock()
time_c = abs(start-end)
print('C function time -> ' + str(time_c))

start = time.clock()
for i in range(test_count):
    temp = a+b
end = time.clock()
time_norm = abs(start-end)
print('numpy time -> ' + str(time_norm))

print('C extension is ' + str(100 * (1 - time_c/time_norm)) + '% faster')

