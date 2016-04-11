A (not yet enough) simple example combining
cffi, numpy, and openMP.

# Running (release mode)

```
OMP_NUM_THREADS=2 python3 -O test.py use_openmp
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
