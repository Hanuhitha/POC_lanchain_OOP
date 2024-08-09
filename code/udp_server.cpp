
#include <iostream>
#include <string>
#include <vector>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

int main() {
    int server_socket;
    struct sockaddr_in server_addr;
    
    // Create a UDP socket
    if ((server_socket = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
        std::cerr << "Error creating socket." << std::endl;
        return 1;
    }
    
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8888);
    server_addr.sin_addr.s_addr = INADDR_ANY;
    
    // Bind the socket to the address and port
    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        std::cerr << "Error binding socket." << std::endl;
        return 1;
    }
    
    while (true) {
        char buffer[1024];
        socklen_t addr_size = sizeof(server_addr);
        
        // Receive data from the client
        ssize_t bytes_received = recvfrom(server_socket, buffer, sizeof(buffer), 0, (struct sockaddr *)&server_addr, &addr_size);
        if (bytes_received == -1) {
            std::cerr << "Error receiving data." << std::endl;
            return 1;
        }
        
        std::string client_message(buffer, bytes_received);
        std::cout << "Received message: " << client_message << std::endl;
        
        // Process the received data as needed
        
        // Send a response back to the client
        const char *response = "Server received the message."