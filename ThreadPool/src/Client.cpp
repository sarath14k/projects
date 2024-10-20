#include "Client.h"  // Include the header file for the Client class

#include <arpa/inet.h>  // Include definitions for internet operations
#include <unistd.h>     // Include Unix standard library for close()

#include <atomic>    // Include for atomic variables
#include <csignal>   // Include for signal handling
#include <cstring>   // Include string manipulation functions
#include <iostream>  // Include standard input/output stream library
#include <thread>    // Include for multithreading

#include "Config.h"     // Include the header file for the Config class
#include "Constants.h"  // Include a header file for constants used in the program
#include "GlobalState.h"  // Include the header for global state management

using namespace constants;  // Use the constants namespace for easier access to
                            // constants

void Client::start() {
  Config config(CONFIG_FILE_PATH);  // Create a Config object to read settings
                                    // from a YAML file
  std::string server_ip =
      config.getClientIP();  // Retrieve the server IP address from the config
  int server_port =
      config
          .getClientPort();  // Retrieve the server port number from the config
  int buffer_size =
      config.getBufferSize();  // Retrieve the buffer size from the config

  std::signal(SIGINT,
              signalHandler);  // Register a signal handler for SIGINT (Ctrl+C)

  // Create a socket for communication
  int sock = socket(AF_INET, SOCK_STREAM, 0);
  if (sock < 0) {  // Check if the socket creation failed
    std::cerr << "Error creating socket."
              << std::endl;  // Print an error message
    return;                  // Exit the start function
  }

  // Define the server address structure
  sockaddr_in server_addr;  // Create a sockaddr_in structure to specify the
                            // server address
  server_addr.sin_family = AF_INET;  // Set the address family to IPv4
  server_addr.sin_port = htons(
      server_port);  // Set the port number (convert to network byte order)
  inet_pton(
      AF_INET, server_ip.c_str(),
      &server_addr.sin_addr);  // Convert the IP address from text to binary

  // Attempt to connect to the server
  if (connect(sock, (sockaddr*)&server_addr, sizeof(server_addr)) <
      0) {  // Try to connect to the server
    std::cerr << "Error connecting to server."
              << std::endl;  // Print an error message if connection fails
    close(sock);             // Close the socket
    return;                  // Exit the start function
  }

    // Start a thread to handle server responses
    std::thread response_thread([&sock]() {
        char response[1024]; // Buffer for server responses
        while (running.load()) {
            ssize_t bytes_received = recv(sock, response, sizeof(response) - 1, 0);
            if (bytes_received > 0) {
                response[bytes_received] = '\0'; // Null-terminate the received string
                std::cout << "Server response: " << response << std::endl;

                // Check for shutdown message
                if (strcmp(response, "Server is shutting down. Closing connection.") == 0) {
                    std::cout << "Server has shut down. Exiting client." << std::endl;
                    running.store(false); // Signal to stop the main loop
                }
            } else if (bytes_received == 0) {
                std::cerr << "Server has closed the connection." << std::endl;
                running.store(false);
                break; // Exit if the connection is lost
            } else {
                std::cerr << "Error receiving data from the server." << std::endl;
                running.store(false);
                break;
            }
        }
    });

  char buffer[buffer_size];  // Create a buffer for message input
  while (running.load()) {
    std::cout << "Enter message (type 'exit' to quit): ";
    std::cin.getline(buffer, buffer_size);  // Get input from user

    if (strcmp(buffer, "exit") == 0) {
      // Send exit message to the server
      ssize_t bytes_sent =
          send(sock, buffer, strlen(buffer), 0);  // Send exit message to server
      if (bytes_sent < 0) {
        std::cerr << "Error sending exit message to the server." << std::endl;
      }
      running.store(false);  // Signal to stop the response thread
      break;                 // Exit the loop if user types "exit"
    }

    // Send the user's message to the server
    ssize_t bytes_sent =
        send(sock, buffer, strlen(buffer), 0);  // Send message to server
    if (bytes_sent < 0) {
      std::cerr
          << "Error sending message to the server. The server may be down."
          << std::endl;
      break;  // Break the loop if there is an error
    }
  }

  // Cleanup
  close(sock);             // Close the socket when done
  response_thread.join();  // Wait for the response thread to finish
  std::cout << "Client has exited." << std::endl;  // Log client exit
}
