Just run test.py!

OpenMP as implemented is really slow (200x slower) than without probably due to thread contention.
Do not use OpenMP as implemented!

# Running (release mode)

```
python3 -O imgsample.py
python3 -O test_add_array_f.py
python3 -O test_add_array_i.py
```

# Running (debug mode)

```
python3 imgsample.py
python3 test_add_array_f.py
python3 test_add_array_i.py
```

# Running On Mac OS X with OpenMP:

`--without-multilib` is mandatory for building with OpenMP support https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60670

```
brew reinstall gcc --without-multilib
USE_OPENMP=true CC=gcc-5 python3 -O test_add_array_f.py
USE_OPENMP=true CC=gcc-5 python3 -O test_add_array_i.py
```

