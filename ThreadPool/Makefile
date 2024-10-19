CC = g++
CFLAGS = -Wall -g
SRC_DIR = src
BIN_DIR = bin
INC_DIR = include
CONFIG = config.yaml

SOURCES = $(wildcard $(SRC_DIR)/*.cpp)                  # Get a list of all .cpp files in the SRC_DIR
OBJECTS = $(patsubst $(SRC_DIR)/%.cpp,$(BIN_DIR)/%.o,$(SOURCES))  # Generate object file names from source files

.PHONY: all clean client-run server-run # Declare phony targets that do not correspond to actual files

all: $(BIN_DIR)/chat            # The default target is 'all', which depends on the final executable

$(BIN_DIR)/chat: $(OBJECTS)      # Define the rule to build the chat executable from object files
	$(CC) -o $@ $^ -lyaml-cpp    # Link the object files and create the chat executable; link against yaml-cpp library

$(BIN_DIR)/%.o: $(SRC_DIR)/%.cpp  # Define the rule to compile .cpp files into .o object files
	@mkdir -p $(BIN_DIR)         # Create the bin directory if it doesn't exist
	$(CC) $(CFLAGS) -I$(INC_DIR) -c $< -o $@  # Compile the source file into an object file

client-run: all                  # Define the target to run the client after building
	@echo "Starting client..."    # Print a message indicating the client is starting
	./$(BIN_DIR)/chat client       # Execute the client with the 'client' argument

server-run: all                  # Define the target to run the server after building
	@echo "Starting server..."     # Print a message indicating the server is starting
	./$(BIN_DIR)/chat server       # Execute the server with the 'server' argument

clean:                           # Define the clean target to remove compiled files
	rm -rf $(BIN_DIR)/*.o $(BIN_DIR)/chat # Remove all object files and the chat executable
