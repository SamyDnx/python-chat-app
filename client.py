import socket
import threading

IP = "127.0.0.1"
PORT = 42069

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

def receive_message():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print(message)
        except:
            print("disconnected from server")
            client.close()
            break

def send_message():
    while True:
        message = input()
        client.send(message.encode())


# run receive_message in parrallel with send_message (main thread)
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

send_message()