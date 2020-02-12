BINARIES = run-mcmc
KORALICXX=$(shell python3 -m korali.cxx --compiler)
KORALICFLAGS=`python3 -m korali.cxx --cflags`
KORALILIBS=`python3 -m korali.cxx --libs`

.SECONDARY:
.PHONY: all
all: $(BINARIES)

run-mcmc : run-mcmc.o
	$(KORALICXX) -o $@ $^ $(KORALILIBS)

%.o: %.cpp
	$(KORALICXX) -c $(KORALICFLAGS) $<

.PHONY: clean
clean:
	$(MAKE) -C model clean
	$(RM) $(BINARIES) *.o *.ti *.optrpt *.txt
