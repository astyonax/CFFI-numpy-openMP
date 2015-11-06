Just run test.py!

OpenMP as implemented is really slow (200x slower) than without probably due to thread contention.
Do not use OpenMP as implemented!

# On Mac OS X without OpenMP:

```
python3 -O test.py
```

# On Mac OS X with OpenMP:

`--without-multilib` is mandatory for building with OpenMP support https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60670

```
brew reinstall gcc --without-multilib
CC=gcc-5 python3 -O test.py use_openmp
```

# On Ubuntu 14.04 with OpenMP:

GCC is the default compiler and it supports OpenMP by default

```
python3 -O test.py use_openmp

```
# On Ubuntu 14.04 without OpenMP:

GCC is the default compiler and it supports OpenMP by default

```
python3 -O test.py
```
