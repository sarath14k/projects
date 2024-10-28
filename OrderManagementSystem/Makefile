# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++11 -Wall -I./include
LDFLAGS = -lcurl -lyaml-cpp

# Directories
SRC_DIR = src
INCLUDE_DIR = include
BIN_DIR = bin

# Target executable
TARGET = $(BIN_DIR)/deribit_order_system

# Source files
SRC_FILES = $(wildcard $(SRC_DIR)/*.cpp)

# Object files
OBJ_FILES = $(SRC_FILES:$(SRC_DIR)/%.cpp=$(BIN_DIR)/%.o)

# Default rule to build the project
all: $(TARGET)

# Linking object files into the final binary
$(TARGET): $(OBJ_FILES)
	$(CXX) $(OBJ_FILES) -o $(TARGET) $(LDFLAGS)

# Compiling each source file into an object file
$(BIN_DIR)/%.o: $(SRC_DIR)/%.cpp | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Create bin directory if it doesn't exist
$(BIN_DIR):
	mkdir -p $(BIN_DIR)

# Clean up
clean:
	rm -rf $(BIN_DIR)/*.o $(TARGET)

.PHONY: all clean
