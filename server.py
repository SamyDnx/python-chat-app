import socket
import threading
import ssl

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

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

clients = []

def handle_client(ssl_client_s):
    """Handle communication with an individual client."""
    while True:
        try:
            message = ssl_client_s.recv(1024).decode('utf-8')
            if message:
                if message[0] == "-":
                    _message = "".join(letter for letter in message if (letter.isalnum() or letter == " "))
                    print("Status event received: ", _message)
                else:
                    print("Message received: ", message)
                broadcast(message, ssl_client_s)
            else:
                clients.remove(ssl_client_s)
                ssl_client_s.close()
                break
        except socket.error as e:
            print(f"Error handling client: {e}")
            clients.remove(ssl_client_s)
            ssl_client_s.close()
            break
        except UnicodeDecodeError as e:
            print("Unicode decoding error:", e)
            clients.remove(ssl_client_s)
            ssl_client_s.close()
            break
        except Exception as e:
            print(f"Unexpected error handling client: {e}")
            clients.remove(ssl_client_s)
            ssl_client_s.close()
            break

def broadcast(message, sender_s):
    """Broadcast a message to all connected clients except the sender."""
    for client in clients:
        if client != sender_s:
            try:
                client.send(message.encode('utf-8'))
            except socket.error as e:
                print(f"Error broadcasting message to client: {e}")
                clients.remove(client)
                client.close()

def start_server():
    """Accept new client connections and wrap them in SSL."""
    while True:
        try:
            client_s, client_addr = serv.accept()
            print("New connection from ", client_addr)

            ssl_client_s = context.wrap_socket(client_s, server_side=True)

            clients.append(ssl_client_s)

            client_thread = threading.Thread(target=handle_client, args=(ssl_client_s,))
            client_thread.start()
        
        except socket.error as e:
            print(f"Error accepting new connection: {e}")
            continue

start_server()
