#ifdef use_openmp
    #include "omp.h"
#endif

#include "stdio.h"

double myadder(double x, double y) {
    return x + y;
}

void add_array(int x, int y, double (*a)[3], double (*b)[3], double (*result)[3]) {
    // collapse(2) needed to parallelize both loops
    #ifdef use_openmp
        #pragma omp parallel for collapse(2)
    #endif
    for(int i = 0; i < x; i++) {
        for(int j = 0; j < y; j++) {
            #ifdef use_openmp
                printf("Thread rank: %d\n", omp_get_thread_num());
            #endif
            result[i][j] = a[i][j] + b[i][j];
        }
    }
}

