#!/bin/bash -x
mkdir -p build
gcc -fPIC -fno-stack-protector -c src/pam/module.c -o build/module.o
sudo ld -x --shared -o /lib/security/pam_voiceprint.so build/module.o
