CC=gcc
CCFLAGS=-O2

TST=./tst
RES=./res
BIN=./bin
LOG=./log
EXT=./ext

TESTS=$(addprefix ${BIN}/, $(notdir $(patsubst %.s,%,$(sort $(wildcard ${TST}/*.s)))))
CROSS_AS=${EXT}/asm6/asm6

all: ${BIN} ${LOG}

asm6:
	${CC} ${CFLAGS} -o ${CROSS_AS} ${EXT}/asm6/asm6.c

${BIN}: asm6
	@mkdir -p ${BIN}

${BIN}/%: ${TST}/%.s
	${CROSS_AS} $^ $@

${LOG}:
	@mkdir -p ${LOG}

test: ${BIN} ${LOG} ${TESTS} asm6
	@{  echo "************************* Tests ******************************"; \
		test_failed=0; \
		test_passed=0; \
		for test in ${TESTS}; do \
			result="${LOG}/$$(basename $$test).log"; \
			expected="${RES}/$$(basename $$test).r"; \
			printf "Running $$test: "; \
			python3 emulator.py $$test > $$result 2>&1;\
			errors=`diff -y --suppress-common-lines $$expected $$result | grep '^' | wc -l`; \
			if [ "$$errors" -eq 0 ]; then \
				printf "\033[0;32mPASSED\033[0m\n"; \
				test_passed=$$((test_passed+1)); \
			else \
				printf "\033[0;31mFAILED [$$errors errors]\033[0m\n"; \
				test_failed=$$((test_failed+1)); \
			fi; \
		done; \
		echo "*********************** Summary ******************************"; \
		echo "- $$test_passed tests passed"; \
		echo "- $$test_failed tests failed"; \
		echo "**************************************************************"; \
	}

unit:
	python3 -m unittest discover .

get_pypy_pygame:
	chmod +x setup_pypy.sh; sudo bash setup_pypy.sh

setup: get_pypy_pygame

clean:
	rm -rf ${BIN}/* ${LOG}/*

clean_pypy_pygame:
	rm -rf pypyenv pypy3.6-v7.2.0-linux64 pypy3.6-v7.2.0-linux64.tar.tar.bz2
