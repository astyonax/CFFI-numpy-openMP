#include "stdlib.h" // import size_t

void sample2d(size_t row_count, size_t column_count, size_t window_size, float *input, float *output) {
    printf("row count-> %zu \n", row_count);
    printf("col count -> %zu \n", column_count);
    printf("window size -> %zu \n", window_size);
    size_t i, j, a, b, output_offset, output_window_offset, output_idx = 0;
    for(i = 0; i < row_count - window_size + 1; i += 1) {
        for(j = 0; j < column_count - window_size + 1; j += 1) {
            //printf("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
            // generate window for current i,j position
            for(a = 0; a < window_size; a++) {
                for(b = 0; b < window_size; b++) {
                    output_offset = window_size * window_size * output_idx;
                    output_window_offset = (window_size * a + b);
                    /*
                    printf("output offset -> %zu \n", output_offset);
                    printf("output window offset -> %zu \n", output_window_offset);
                    printf("output_idx -> %zu \n", output_idx);
                    
                    printf("\n"); 
                    printf("input[column_count * (i + a) + (j + b)] -> %2.2f \n", input[column_count * (i + a) + (j + b)]);
                    printf("i -> %zu \n", i);
                    printf("a -> %zu \n", a);
                    printf("j -> %zu \n", j);
                    printf("b -> %zu \n", b);
                    */
                    output[output_offset + output_window_offset] = input[column_count * (i + a) + (j + b)];
                }
            }
            output_idx += 1;
        }
    }
}

