CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -I/usr/include/FL -I/usr/include
LDFLAGS = -L/usr/lib -lfltk -lssl -lcrypto

SOURCES = main.cpp gui.cpp rsaEncryptor.cpp
EXECUTABLE = encryption_tool

all: $(EXECUTABLE)

$(EXECUTABLE): $(SOURCES)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)

clean:
	rm -f $(EXECUTABLE)
