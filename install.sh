#!/bin/bash
mkdir -p build
gcc -fPIC -fno-stack-protector -c src/pam/module.c -o build/module.o
gcc -fPIC -fno-stack-protector -c src/bridge/py_identify_bridge.c -I /usr/include/python3.10 -o build/py_identify_bridge.o
sudo ld -x --shared -o /lib/security/pam_voiceprint.so build/*.o 
