import socket
import threading
import random

messages = []
connected_clients = []
MAX_CONNECTION = 3

history_file = open("history_messages.txt", "r+")
history = history_file.readlines()
encryption_key = random.randint(1, 50)


def send_encryption_key(client_connection):
    client_connection.send(str(encryption_key).encode())


def init_client_connection(client_connection):
    send_encryption_key(client_connection)
    send_history(client_connection)
    handle_client_messages(client_connection)


def decryption(message_to_decrypt):
    decrypted_message = ''
    for char in message_to_decrypt:
        decrypted_message += chr(ord(char) - encryption_key)


def handle_client_messages(client_connection):
    while True:
        try:
            data = client_connection.recv(1024).decode()
        except ConnectionResetError:
            break

        if not data:
            break
        send_message_to_all_clients(data)
        decryption(data)
        history.append(data)
        history_file.write(data)
        history_file.flush()


def send_history(client_connection):
    for message in history:
        client_connection.send(message.encode())


def send_message_to_all_clients(message: str):
    for client in connected_clients:
        try:
            client.send(message.encode())
        except OSError:
            print("OSError")
            connected_clients.remove(client)


def start_server_program():
    host = socket.gethostbyname('localhost')
    port = 9092

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(MAX_CONNECTION)

    while True:
        new_connection, _ = server_socket.accept()
        threading.Thread(target=init_client_connection, args=(new_connection,)).start()
        connected_clients.append(new_connection)


if __name__ == '__main__':
    start_server_program()
