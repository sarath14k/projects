# Makefile for Multi-threaded Web Server

# Compiler
CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -Iinclude -I/usr/include  # Include path to yaml-cpp headers

# Linker flags
LDFLAGS = -lyaml-cpp  # Link against yaml-cpp

# Source and header files
SRCS = src/main.cpp src/Server.cpp src/ThreadPool.cpp src/Config.cpp
OBJS = $(patsubst src/%.cpp, $(OBJ_DIR)/%.o, $(SRCS))  # Object files with path

# Executable name
TARGET = MultiThreadedWebServer

# Output directories
BIN_DIR = bin
OBJ_DIR = obj

# Ensure output directories exist
$(BIN_DIR) $(OBJ_DIR):
	mkdir -p $@  # Use a tab for indentation

# Default target to build the executable
all: $(BIN_DIR)/$(TARGET)

# Rule to link object files into the final executable
$(BIN_DIR)/$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)  # Link with yaml-cpp

# Rule to compile source files into object files
$(OBJ_DIR)/%.o: src/%.cpp | $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Rule to clean up the directory (remove object files and executable)
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)/$(TARGET)  # Use -rf to remove directories and files without prompting

# Rule to run the server
run: $(BIN_DIR)/$(TARGET)
	./$(BIN_DIR)/$(TARGET)

# Phony targets (not files)
.PHONY: all clean run
