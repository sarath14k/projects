CC = g++
CFLAGS = -Wall -g
SRC_DIR = src
BIN_DIR = bin
INC_DIR = include
CONFIG = config.yaml

SOURCES = $(wildcard $(SRC_DIR)/*.cpp)
OBJECTS = $(patsubst $(SRC_DIR)/%.cpp,$(BIN_DIR)/%.o,$(SOURCES))

.PHONY: all clean client-run server-run

all: $(BIN_DIR)/chat

$(BIN_DIR)/chat: $(OBJECTS)
	$(CC) -o $@ $^ -lyaml-cpp

$(BIN_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) -I$(INC_DIR) -c $< -o $@

client-run: all
	@echo "Starting client..."
	./bin/chat client

server-run: all
	@echo "Starting server..."
	./bin/chat server

clean:
	rm -rf $(BIN_DIR)/*.o $(BIN_DIR)/chat
