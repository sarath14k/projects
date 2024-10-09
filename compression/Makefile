# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -std=c++17 -Wall -Iinclude

# Directories
SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin
INC_DIR = include

# Source files
SRC_FILES = $(wildcard $(SRC_DIR)/*.cpp)
OBJ_FILES = $(SRC_FILES:$(SRC_DIR)/%.cpp=$(OBJ_DIR)/%.o)

# Executable
TARGET = $(BIN_DIR)/FileCompressionTool

# Rules
all: $(TARGET)

$(TARGET): $(OBJ_FILES)
	$(CXX) $(OBJ_FILES) -o $@ -lsfml-graphics -lsfml-window -lsfml-system

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Run rule
run: $(TARGET)
	./$(TARGET)

# Clean rule
clean:
	rm -f $(OBJ_DIR)/*.o $(TARGET)

.PHONY: all run clean
