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

# window size 2

my_input = numpy.array(
    [
        [1,   2,  3,  4],
        [5,   6,  7,  8],
        [9,  10, 11, 12],
        [13, 14, 15, 16],
    ], dtype=numpy.float32
)

window_size = 2
sample_count = (my_input.shape[0]-1) * (my_input.shape[1]-1)
my_output = numpy.zeros((sample_count, window_size, window_size), dtype=numpy.float32)

_x = _imgsample.ffi.cast('size_t', my_input.shape[0])
_y = _imgsample.ffi.cast('size_t', my_input.shape[1])
_window_size = _imgsample.ffi.cast('size_t', window_size)
_my_input = _imgsample.ffi.cast('float *', _imgsample.ffi.from_buffer(my_input))
_my_output = _imgsample.ffi.cast('float *', _imgsample.ffi.from_buffer(my_output))

_imgsample.lib.sample(_x, _y, _window_size, _my_input, _my_output)
assert numpy.array_equal(my_output[0], [[1,2],[5,6]])
assert numpy.array_equal(my_output[sample_count-1], [[11,12],[15,16]])

# window size 3

