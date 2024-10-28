CXX = g++
CXXFLAGS = -Iinclude -Iconfig -std=c++17
LDFLAGS = -lcurl

SRC = src/main.cpp src/deribit_api.cpp
OBJ = $(SRC:.cpp=.o)
TARGET = deribit_trading

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CXX) -o $@ $^ $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# New target to run the executable
run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(OBJ) $(TARGET)
