import numpy
##############################################
######## Configuration
## Array type
CDTYPE,PYDTYPE=('float' ,numpy.float32) ## this is the type we use on pyopencl
CDTYPE,PYDTYPE=('double',numpy.float64)
## Array size
N=1024*5
## Number of test runs
test_count = 10
###############################################
a = numpy.array(
    [
        [1, 2, 3, 4, 5, 6],
        [4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 5, 6],
        [4, 5, 6, 7, 8, 9],
    ], dtype=PYDTYPE
)

b = numpy.array(
    [
        [4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 5, 6],
        [6, 5, 4, 3, 1, 2],
        [1, 2, 3, 4, 5, 6],
    ], dtype=PYDTYPE
)
result = numpy.zeros_like(a)

import sys
use_openmp = True
try:
    if sys.argv[1] == 'use_openmp':
        use_openmp = True
except IndexError:
    pass

import cffi
ffi = cffi.FFI()
with open('test.h') as my_header:
    ffi.cdef(my_header.read().replace('CDTYPE',CDTYPE))

with open('test.c') as my_source:
    if __debug__:
        print('Building the debug build...')
        ffi.set_source(
            '_test',
            my_source.read().replace('CDTYPE',CDTYPE),
            extra_compile_args=[ '-pedantic', '-Wall', '-g', '-O0']
        )
    else:
        if use_openmp:
            print('Building for performance with OpenMP...')
            ffi.set_source(
                '_test',
                my_source.read().replace('CDTYPE',CDTYPE),
                extra_compile_args=['-fopenmp', '-D use_openmp', '-Ofast','-march=native','-ffast-math'],
                extra_link_args=['-fopenmp'],
            )
        else:
            print('Building for performance without OpenMP...')
            ffi.set_source('_test', my_source.read(), extra_compile_args=['-Ofast','-march=native','-ffast-math'],)

ffi.compile()  # convert and compile - mandatory!

import _test

assert (_test.lib.myadder(10,12)) - (10+12) < 0.01  # A - B < 0.1 if A ~= B

# _test.ffi.from_buffer(my_array) is a less verbose alternative to:
# my_array.__array_interface__['data'][0]
_x = _test.ffi.cast('size_t', a.shape[0])
_y = _test.ffi.cast('size_t', a.shape[1])
_a = _test.ffi.cast('{0:s} *'.format(CDTYPE), _test.ffi.from_buffer(a))
_b = _test.ffi.cast('{0:s} *'.format(CDTYPE), _test.ffi.from_buffer(b))
_result = _test.ffi.cast('{0:s} *'.format(CDTYPE), _test.ffi.from_buffer(result))

_test.lib.add_array(_x, _y, _a, _b, _result)

assert numpy.array_equal(numpy.add(a,b), result)
print('Test 1 OK!')

a = numpy.random.rand(N,N).astype(PYDTYPE)
b = numpy.random.rand(N,N).astype(PYDTYPE)
result = numpy.zeros_like(a)

_x = _test.ffi.cast('size_t', a.shape[0])
_y = _test.ffi.cast('size_t', a.shape[1])
_a = _test.ffi.cast('{0:s} *'.format(CDTYPE), _test.ffi.from_buffer(a))
_b = _test.ffi.cast('{0:s} *'.format(CDTYPE), _test.ffi.from_buffer(b))
_result = _test.ffi.cast('{0:s} *'.format(CDTYPE), _test.ffi.from_buffer(result))

_test.lib.add_array(_x, _y, _a, _b, _result)
assert numpy.array_equal(numpy.add(a,b), result)
print('Test 2 OK! -- {0:d}x{0:d} '.format(N))

# import timeit
# number=100
# time_c=timeit.timeit(lambda : _test.lib.add_array(_x, _y, _a, _b, _result),number=number)/number
# time_np=timeit.timeit(lambda : a+b,number=number)/number
# print('C  function time {0:.5f} s/call'.format(time_c))
# print('NP function time {0:.5f} s/call'.format(time_np))

import time

start = time.clock()
for i in range(test_count):
    temp = a+b
end = time.clock()
time_norm = abs(start-end)/test_count
print('numpy time -> ' + str(time_norm) + ' s/call')

start = time.clock()
for i in range(test_count):
    _test.lib.add_array(_x, _y, _a, _b, _result)
end = time.clock()
time_c = abs(start-end)/test_count
print('C time -> ' + str(time_c) + ' s/call')

print('C extension is ' + str(100 * (1 - time_c/time_norm)) + '% faster')
