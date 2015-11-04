import cffi

ffi = cffi.FFI()
with open('test.h') as my_header:
    ffi.cdef(my_header.read())
with open('test.c') as my_source:
    ffi.set_source('_test', my_source.read(), libraries=[])

ffi.compile()  # convert and compile - mandatory!

import _test
assert (_test.lib.myadder(10,12)) - (10+12) < 0.01  # A - B < 0.1 if A ~= B
print('All OK!')
