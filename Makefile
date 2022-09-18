CLASSES = bridge/py_identify_bridge
SRC_FILES = pam/test

PFX_DIR = src/
OBJ_DIR = build/
CC = gcc
CFLAGS = -fPIC -fno-stack-protector -c -I/usr/include/python3.10 -I/usr/include/python3.10  -Wno-unused-result -Wsign-compare -march=x86-64 -mtune=generic -O3 -pipe -fno-plt -fexceptions         -Wp,-D_FORTIFY_SOURCE=2 -Wformat -Werror=format-security         -fstack-clash-protection -fcf-protection -g -ffile-prefix-map=/build/python/src=/usr/src/debug -flto=auto -ffat-lto-objects -DNDEBUG -g -fwrapv -O3 -Wall
PFX_CLASSES = $(addprefix ${PFX_DIR}, ${CLASSES})
PFX_SRC_FILES = $(addprefix ${PFX_DIR}, ${SRC_FILES})
OBJECTS = $(addsuffix .o, ${PFX_CLASSES} ${PFX_SRC_FILES})
DEPENDS = ${OBJECTS:.o=.d}

test: ${OBJECTS}
	${CC} ${CCFLAGS} ${OBJECTS} -o build/test -L/usr/lib -lpython3.10 -lcrypt -ldl  -lm -lm

dist: ${OBJECTS}
	${CC} ${CCFLAGS} ${OBJECTS} -shared -o build/pam_voiceprint.so -L/usr/lib -lpython3.10 -lcrypt -ldl  -lm -lm
	

-include ${DEPENDS}

.PHONY: clean install

clean:
	rm ${OBJECTS} ${DEPENDS}

install:
	cp build/pam_voiceprint.so /lib/security/
