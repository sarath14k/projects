# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -std=c++17 -Wall

# SFML Libraries (adjust the path to your SFML installation if necessary)
LIBS = -lsfml-graphics -lsfml-window -lsfml-system

# Directories
SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin

# Source and object files
SRCS = $(wildcard $(SRC_DIR)/*.cpp)
OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRCS))

# Executable file
TARGET = $(BIN_DIR)/AlgorithmVisualizer

# Default target
all: $(TARGET)

# Rule to compile the target
$(TARGET): $(OBJS) | $(BIN_DIR)
	$(CXX) $(OBJS) -o $(TARGET) $(LIBS)

# Rule to compile object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp | $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Create directories if they don't exist
$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

# Clean build files
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)

# Phony target to avoid conflicts with files of the same name
.PHONY: all clean

