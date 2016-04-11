A (not yet enough) simple example combining
cffi, numpy, and openMP.

# Running (release mode)

```
$ OMP_NUM_THREADS=2 python3 -O test.py use_openmp
Building for performance with OpenMP...
Test 1 OK!
Test 2 OK! -- 5120x5120
numpy time -> 0.1006176 s/call
C time -> 0.0816459 s/call
C extension is 18.8552499761% faster
```

# Running (debug mode)

```
python3 test.py
```

From the original documentation
>## Running On Mac OS X with OpenMP:
>`--without-multilib` is mandatory for building with OpenMP support https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60670
>```
>brew reinstall gcc --without-multilib
>USE_OPENMP=true CC=gcc-5 python3 -O test_add_array_f.py
>USE_OPENMP=true CC=gcc-5 python3 -O test_add_array_i.py
>```
