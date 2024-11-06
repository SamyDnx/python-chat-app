import socket
import threading

IP = "127.0.0.1"
PORT = 42069

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((IP, PORT))
serv.listen(3)
print(f"server listening on {IP}:{PORT}")

clients = []

def handle_client(client_s):
    """
    Handle messages from client
    """
    while True:
        try:
            message = client_s.recv(1024).decode()
            if message:
                print("message received: ", message)
                broadcast(message, client_s)
            else:
                clients.remove(client_s)
                client_s.close()
                break
        except:
            clients.remove(client_s)
            client_s.close()
            break

def broadcast(message, sender_s):
    for client in clients:
        if client != sender_s:
            client.send(message.encode())

def start_server():
    """
    Accept client connection and open a new thread for each client
    """
    while True:
        client_s, client_addr = serv.accept()
        print("New connection from ", client_addr)
        clients.append(client_s)
        # start new thread
        client_thread = threading.Thread(target=handle_client, args=(client_s,))
        client_thread.start()

start_server()