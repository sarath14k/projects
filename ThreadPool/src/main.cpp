#include "Client.h"
#include "Server.h"
#include <iostream>
#include "Constants.h"
using namespace Constants;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <server|client>" << std::endl;
        return 1;
    }

    if (std::string(argv[1]) == SERVER) {
        Server server;
        server.start();
    } else if (std::string(argv[1]) == CLIENT) {
        Client client;
        client.start();
    } else {
        std::cerr << "Invalid argument. Use 'server' or 'client'." << std::endl;
        return 1;
    }

    return 0;
}
