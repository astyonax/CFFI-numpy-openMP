#ifdef use_openmp
    #include "omp.h"
#endif

#include "stdio.h" // import printf
#include "stdlib.h" // import size_t

void add_array( const size_t row_count, const size_t column_count, CDTYPE *a, CDTYPE *b, CDTYPE *result) {

    size_t idx;
    #ifdef use_openmp
        #pragma omp for collapse(2) private(idx) // This is openmp 3.0
    #endif
    for(size_t i = 0; i < row_count; i++) {
      for(size_t j = 0; j < column_count; j++) {
            idx = column_count * i + j;
            result[idx] = a[idx] + b[idx];
        }
    }
}
