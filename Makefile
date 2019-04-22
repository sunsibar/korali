INCLUDES = $(shell cd source && find . | grep "\.h")
TESTS = $(dir $(wildcard tests/*/))
CURDIR = $(shell pwd)

include korali.config

.PHONY: all install clean snapshot tests clean_tests $(TESTS)

all: source/libkorali.so

source/libkorali.so: libs/gsl/lib/libgsl.so
	@$(MAKE) -j -C source

clean: clean_tests
	@$(MAKE) -j -C source clean

tests: $(TESTS)

$(TESTS):: install
	$(MAKE) -j -C $@

clean_tests:
	for i in $(TESTS); do $(MAKE) -j -C $$i clean; done

install: source/libkorali.so
	@echo "[Korali] Installing Korali..."
	mkdir -p $(PREFIX)/lib
	mkdir -p $(PREFIX)/include
	mkdir -p $(PREFIX)/bin
	cp source/libkorali.so $(PREFIX)/lib
	cp source/libkorali.a $(PREFIX)/lib
	@cd source && cp $(INCLUDES) --parents $(PREFIX)/include
	cp libs/json -r $(PREFIX)/include
	cp libs/koralijson -r $(PREFIX)/include
	cp libs/gsl -r $(PREFIX)/lib/koraligsl
	@echo "#!/bin/bash" > $(PREFIX)/bin/korali-cxx
	@cat korali.config tools/korali-cxx >> $(PREFIX)/bin/korali-cxx
	@chmod a+x  $(PREFIX)/bin/korali-cxx
	@echo '------------------------------------------------------------------'
	@echo '[Korali] To complete installation, please update your environment:'
	@echo '[Korali] >export PATH=$$PATH:$(PREFIX)/bin'
	@echo '[Korali] >export PYTHONPATH=$$PYTHONPATH:$(PREFIX)/lib'
	@echo '------------------------------------------------------------------' 

snapshot: install clean
	tar -zcvf korali`date +"%m-%d-%y"`.tar.gz korali/ tests/

libs/gsl/lib/libgsl.so:
	@echo "[Korali] Downloading and Compiling GNU Scientific Library... "
	cd libs/ && rm -f gsl-2.5.tar.gz && wget "ftp://ftp.gnu.org/gnu/gsl/gsl-2.5.tar.gz" && tar -xzvf gsl-2.5.tar.gz > /dev/null 2>&1
	cd libs/gsl-2.5 && ./configure --prefix=$(CURDIR)/libs/gsl && make && make install
	rm -rf libs/gsl-2.5 libs/gsl-2.5.tar.gz
