#ifdef use_openmp
    #include "omp.h"
#endif

#include "stdio.h"

double myadder(double x, double y) {
    return x + y;
}

void add_array(int x, int y, double (*a)[y], double (*b)[y], double (*result)[y]) {
    // collapse(2) needed to parallelize both loops
    #ifdef use_openmp
        #pragma omp parallel for
    #endif
    for(int i = 0; i < x; i++) {
        for(int j = 0; j < y; j++) {
            result[i][j] = a[i][j] + b[i][j];
        }
    }
}

