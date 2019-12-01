CXX = g++
CXXFLAG = -W -Wall -g
LIB = -lm -lgsl -lgslcblas

SRC1 = src/rtnorm.cpp 
OBJ1 = tmp/rtnorm.o

HDRS = src/rtnorm.hpp

all : $(OBJ1)

$(OBJ1) : $(SRC1) $(HDRS)
	$(CXX) -o $(OBJ1) -c $(SRC1) $(CXXFLAG)

clean : 
	rm -rf ./tmp/*.o
