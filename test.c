#ifdef use_openmp
    #include "omp.h"
#endif

#include "stdio.h"

double myadder(double x, double y) {
    return x + y;
}

void add_array(int row_count, int column_count, double *a, double *b, double *result) {
    // collapse(2) needed to parallelize both loops
    #ifdef use_openmp
        #pragma omp parallel for
    #endif
    for(int i = 0; i < row_count; i++) {
        for(int j = 0; j < column_count; j++) {
            *(result + column_count * i + j) = *(a + column_count * i + j) + *(b + column_count * i + j);
        }
    }
}

