#!/bin/bash
mkdir -p build
cd src/pam
gcc -fPIC -fno-stack-protector -c module.c -o ../../build/module.o
gcc -fPIC -fno-stack-protector -c ../bridge/py_identify_bridge.c -I /usr/include/python3.10 -o ../../build/py_identify_bridge.o
sudo ld -x --shared -o /lib/security/pam_voiceprint.so ../../build/*.o 
