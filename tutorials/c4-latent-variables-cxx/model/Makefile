all: model.o, load_data.o
KORALICXX=$(shell python3 -m korali.cxx --compiler)
KORALICFLAGS=`python3 -m korali.cxx --cflags`

load_data.o: load_data.cpp , load_data.hpp
	$(KORALICXX) -c $< $(KORALICFLAGS)


model.o: load_data.hpp, model.hpp
	$(KORALICXX) -c $< $(KORALICFLAGS)

clean:; rm -rf $(TARGET) *.o

.PHONY: clean all
