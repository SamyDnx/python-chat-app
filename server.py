import socket
import threading

IP = "127.0.0.1"
PORT = 42069

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serv.bind((IP, PORT))
except socket.error as e:
    print(f"Error binding socket to {IP}:{PORT}: {e}")
    exit(1)

try:
    serv.listen(3)
except socket.error as e:
    print(f"Error starting server listener: {e}")
    exit(1)

print(f"Server listening on {IP}:{PORT}")

clients = []

def handle_client(client_s):
    while True:
        try:
            message = client_s.recv(1024).decode()
            if message:
                if message[0] == "-":
                    _message = "".join(letter for letter in message if (letter.isalnum() or letter == " "))
                    print("status event received: ", _message)
                else:
                    print("message received: ", message)
                broadcast(message, client_s)
            else:
                clients.remove(client_s)
                client_s.close()
                break
        except socket.error as e:
            print(f"Error handling client: {e}")
            clients.remove(client_s)
            client_s.close()
            break
        except Exception as e:
            print(f"Unexpected error handling client: {e}")
            clients.remove(client_s)
            client_s.close()
            break

def broadcast(message, sender_s):
    for client in clients:
        if client != sender_s:
            try:
                client.send(message.encode())
            except socket.error as e:
                print(f"Error broadcasting message to client: {e}")
                clients.remove(client)
                client.close()

def start_server():
    while True:
        try:
            client_s, client_addr = serv.accept()
        except socket.error as e:
            print(f"Error accepting new connection: {e}")
            continue

        print("New connection from ", client_addr)
        clients.append(client_s)
        client_thread = threading.Thread(target=handle_client, args=(client_s,))
        client_thread.start()

start_server()