Just run test.py!

# On Mac OS X without OpenMP:

```
python3 test.py
```

# On Mac OS X with OpenMP:

```
# --without-multilib is mandatory for building
# with OpenMP support https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60670
brew reinstall gcc --without-multilib
CC=gcc-5 python3 test.py use_openmp
```

# On Ubuntu 14.04:

GCC is the default compiler and it supports OpenMP by default

```
python3 test.py use_openmp
```
