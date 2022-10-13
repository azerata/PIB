from distutils import ccompiler
from ctypes import CDLL, c_char_p

filename = "hello"

# Initiate a ccompiler object, we can add files, paths and links to this object
# So that they are always included
comp = ccompiler.new_compiler()

# compile a file, return list of strings with compiled files
files = comp.compile(["hello.c"])

# get the shared lib name of a file
libname = comp.library_filename(filename)

# Create shared library from list of files, give the shared library a name.
comp.link_shared_lib(files, filename)

# using ctypes import shared library
lib = CDLL("./libhello.so")

# acces the function "hello", from library lib
hello = lib.hello

# set ´return type of the function hello / default is c_int
hello.restype = c_char_p

# function call and print.
out = hello()

print(type(out))
print(out)
