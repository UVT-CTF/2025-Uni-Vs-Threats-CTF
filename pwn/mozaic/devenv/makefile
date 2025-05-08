DATA_FILE:=./src/data.c
DATA_FILE_OUT:=./var/data.o
BUILD_FILES:=$(wildcard ./src/*.c)
BUILD_FILES:=$(filter-out ${DATA_FILE}, $(BUILD_FILES))
COMMON_FLAGS:= -nostdlib -masm=intel -static -Wall -fno-stack-protector
DEBUG_FLAGS:=-ggdb3
RELEASE_FLAGS:=-O1
OUTFILE:=./bin/mozaic
OUT_SYSCALLS=./var/syscalls.o

all:
	$(MAKE) release
	$(MAKE) obj

run:
	${OUTFILE}

syscalls:
	nasm -f elf64 ./src/syscalls.asm -o ${OUT_SYSCALLS}

data:
	gcc ${COMMON_FLAGS} ${DATA_FILE} -c -o ${DATA_FILE_OUT}

debug:
	$(MAKE) syscalls
	$(MAKE) data
	gcc ${COMMON_FLAGS} ${BUILD_FILES} ${OUT_SYSCALLS} ${DATA_FILE_OUT} -o ${OUTFILE} ${DEBUG_FLAGS}

release:
	$(MAKE) syscalls
	$(MAKE) data
	gcc ${COMMON_FLAGS} ${BUILD_FILES} ${OUT_SYSCALLS} ${DATA_FILE_OUT} -o ${OUTFILE} ${RELEASE_FLAGS}

pwn:
	python3 ./sol/sol.py

obj:
	objdump -M intel -d ${OUTFILE} &> ./var/objdump.asm