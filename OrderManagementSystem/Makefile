CXX = g++
CXXFLAGS = -Iinclude -Iconfig -std=c++17
LDFLAGS = -lcurl

SRC = src/main.cpp src/deribit_api.cpp
OBJ = $(SRC:src/%.cpp=bin/%.o)  # Update to place object files in bin/
TARGET = deribit_trading

# Create the bin directory if it doesn't exist
$(shell mkdir -p bin)

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CXX) -o $@ $^ $(LDFLAGS)

bin/%.o: src/%.cpp  # Adjust pattern rule to match source files
	$(CXX) $(CXXFLAGS) -c $< -o $@

# New target to run the executable
run: $(TARGET)
	./$(TARGET)

clean:
	rm -f bin/*.o $(TARGET)  # Clean up object files in bin/
