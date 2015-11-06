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

window_size = 2

my_input = numpy.array(
    [
        [1,   2,  3,  4],
        [5,   6,  7,  8],
        [9,  10, 11, 12],
        [13, 14, 15, 16],
    ], dtype=numpy.float32
)
my_output = numpy.zeros((9, 2, 2,), dtype=numpy.float32)

_x = _imgsample.ffi.cast('size_t', my_input.shape[0])
_y = _imgsample.ffi.cast('size_t', my_input.shape[1])
_window_size = _imgsample.ffi.cast('size_t', window_size)
_input = _imgsample.ffi.cast('float *', _imgsample.ffi.from_buffer(my_input))
_output = _imgsample.ffi.cast('float *', _imgsample.ffi.from_buffer(my_output))

_imgsample.lib.sample10(_x, _y, _window_size, _input, _output)
assert numpy.arrayequal(output[0], [[1,2],[3,4]])
print('final ->')
print(my_input)
print(my_input.shape)
print(my_output)
print(my_output.shape)
