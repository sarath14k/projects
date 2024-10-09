CXX = g++
CXXFLAGS = -I/usr/include -Iinclude -std=c++11
LDFLAGS = -L/usr/lib -lfltk -lavcodec -lavformat -lavutil -lswscale -lswresample -lavdevice

SRC_DIR = src
INC_DIR = include
BIN_DIR = bin

# List all source files and generate the corresponding object files in the bin directory
SOURCES = $(wildcard $(SRC_DIR)/*.cpp)
OBJECTS = $(patsubst $(SRC_DIR)/%.cpp,$(BIN_DIR)/%.o,$(SOURCES))

TARGET = $(BIN_DIR)/MediaPlayer

# Default target: build the executable
all: $(TARGET)

# Ensure the bin directory exists and link all object files to create the executable
$(TARGET): $(OBJECTS)
	@mkdir -p $(BIN_DIR)
	$(CXX) $(OBJECTS) -o $@ $(LDFLAGS)

# Compile each source file into an object file, store objects in the bin directory
$(BIN_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean rule to remove the object files and the target executable
clean:
	rm -rf $(BIN_DIR)/*.o $(TARGET)

# Run the MediaPlayer executable
run: all
	$(TARGET)

.PHONY: all clean run
