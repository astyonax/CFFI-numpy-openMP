double myadder(double x, double y) {
    return x + y;
}

void add_array(int x, int y, double (*a)[3], double (*b)[3], double (*result)[3]) {
    for(int i = 0; i < x; i++) {
        for(int j = 0; j < y; j++) {
            result[i][j] = a[i][j] + b[i][j];
        }
    }
}
