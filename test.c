#ifdef use_openmp
    #include "omp.h"
#endif

#include "stdio.h" // import printf
#include "stdlib.h" // import size_t

float myadder(float x, float y) {
    return x + y;
}

void add_array_f(size_t row_count, size_t column_count, float *a, float *b, float *result) {
    size_t idx;

    // collapse(2) needed to parallelize both loops
    #ifdef use_openmp
        #pragma omp parallel for
    #endif
    for(size_t i = 0; i < row_count; i++) {
        for(size_t j = 0; j < column_count; j++) {
            idx = column_count * i + j;
            result[idx] = a[idx] + b[idx];
        }
    }
}

void add_array_i(size_t row_count, size_t column_count, int *a, int *b, int *result) {
    size_t idx;

    // collapse(2) needed to parallelize both loops
    #ifdef use_openmp
        #pragma omp parallel for
    #endif
    for(size_t i = 0; i < row_count; i++) {
        for(size_t j = 0; j < column_count; j++) {
            idx = column_count * i + j;
            result[idx] = a[idx] + b[idx];
        }
    }
}

