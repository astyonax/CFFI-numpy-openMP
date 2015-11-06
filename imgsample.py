import numpy
import cffi
ffi = cffi.FFI()

with open('imgsample.h') as my_header:
    ffi.cdef(my_header.read())

with open('imgsample.c') as my_source:
    if __debug__:
        print('Building the debug build...')
        ffi.set_source(
            '_imgsample',
            my_source.read(),
            extra_compile_args=['-Werror', '-pedantic', '-Wall', '-g', '-O0']
        )
    else:
        print('Building for performance without OpenMP...')
        ffi.set_source(
            '_imgsample',
            my_source.read(),
            extra_compile_args=['-Ofast']
        )

ffi.compile()  # convert and compile - mandatory!

import _imgsample

my_input = numpy.random.rand(512,512).astype(numpy.float32)
my_output = numpy.random.rand(512,512).astype(numpy.float32)

_x = _imgsample.ffi.cast('size_t', my_input.shape[0])
_y = _imgsample.ffi.cast('size_t', my_input.shape[1])
_input = _imgsample.ffi.cast('float *', _imgsample.ffi.from_buffer(my_input))
_output = _imgsample.ffi.cast('float *', _imgsample.ffi.from_buffer(my_output))

_imgsample.lib.sample(_x, _y, _input, _output)
assert numpy.array_equal(my_input, my_output)
