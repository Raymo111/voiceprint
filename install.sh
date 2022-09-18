#!/bin/bash
mkdir -p build
cd src/pam
gcc -fPIC -fno-stack-protector -c module.c -o ../../build/module.o
gcc -fPIC -fno-stack-protector -c ../bridge/py_identify_bridge.c -I /usr/include/python3.10 -o ../../build/py_identify_bridge.o -Wno-unused-result -Wsign-compare -march=x86-64 -mtune=generic -O3 -pipe -fno-plt -fexceptions         -Wp,-D_FORTIFY_SOURCE=2 -Wformat -Werror=format-security         -fstack-clash-protection -fcf-protection -g -ffile-prefix-map=/build/python/src=/usr/src/debug -flto=auto -ffat-lto-objects -DNDEBUG -g -fwrapv -O3 -Wall -L/usr/lib -lpython3.10 -lcrypt -ldl  -lm -lm
sudo ld -x --shared -o /lib/security/pam_voiceprint.so ../../build/*.o
