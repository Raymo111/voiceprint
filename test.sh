#!/bin/bash
mkdir -p build
cd src/pam/
gcc -fPIC -fno-stack-protector test.c ../bridge/py_identify_bridge.c -o ../../build/test -I /usr/include/python3.10 -Wno-unused-result -Wsign-compare -march=x86-64 -mtune=generic -O3 -pipe -fno-plt -fexceptions         -Wp,-D_FORTIFY_SOURCE=2 -Wformat -Werror=format-security         -fstack-clash-protection -fcf-protection -g -ffile-prefix-map=/build/python/src=/usr/src/debug -flto=auto -ffat-lto-objects -DNDEBUG -g -fwrapv -O3 -Wall -L/usr/lib -lpython3.10 -lcrypt -ldl  -lm -lm
# ld -x -o build/test build/{test,py_identify_bridge}.o
