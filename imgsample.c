#include "stdlib.h" // import size_t

void sample10(size_t row_count, size_t column_count, size_t window_size, float *input, float *output) {
    printf("row count-> %zu \n", row_count);
    printf("col count -> %zu \n", column_count);
    printf("window size -> %zu \n", window_size);
    size_t i, j, a, b, output_idx = 0;
    for(i = 0; i < row_count - 1; i += 1) {
        for(j = 0; j < column_count - 1; j += 1) {
            // generate window for current i,j position
            for(a = 0; a < window_size; a++) {
                for(b = 0; b < window_size; b++) {
                    printf("input[column_count * (i + a) + (j + b)] -> %2.6f \n", input[column_count * (i + a) + (j + b)]);
                    printf("i -> %zu \n", i);
                    printf("a -> %zu \n", a);
                    printf("j -> %zu \n", j);
                    printf("b -> %zu \n", b);
                    output[output_idx * (column_count * (i + a) + (j + b))] = input[column_count * (i + a) + (j + b)];
                }
            }
            output_idx += 1;
            printf("output_idx -> %zu \n", output_idx);
        }
    }
}

