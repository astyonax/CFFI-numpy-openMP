#include "stdlib.h" // import size_t

void sample(size_t row_count, size_t column_count, float *input, float *output) {
    size_t idx;
    for(size_t i = 0; i < row_count; i++) {
        for(size_t j = 0; j < column_count; j++) {
            idx = column_count * i + j;
            output[idx] = input[idx];
        }
    }
}

