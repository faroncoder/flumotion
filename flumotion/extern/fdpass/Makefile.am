common_cflags = -Wall -fPIC
common_ldflags = -module -avoid-version

flumotiondir = $(libdir)/flumotion/python/flumotion/extern/fdpass

flumotion_PROGRAMS = fdpass.so

flumotion_PYTHON = __init__.py

INCLUDES = $(PYTHON_INCLUDES)

fdpass_so_CFLAGS = $(common_cflags)
fdpass_so_LDFLAGS = $(common_ldflags)
fdpass_so_SOURCES = fdpass.c
fdpass_so_LINK = $(CC) -shared -o fdpass.so

clean-local:
	rm -rf *.pyc *.pyo

EXTRA_DIST = $(flumotion_PYTHON)

