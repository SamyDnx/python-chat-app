import socket
import threading

IP = "127.0.0.1"
PORT = 42069

username = input("Enter your usename: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

message = f"---{username} entered the chat---"
client.send(message.encode())

def receive_message():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print("\r", message)
                print(f"\r{username}: ", end="")
        except:
            print("\rdisconnected from server")
            client.close()
            break

def send_message():
    while True:
        message = input(username + ": ")
        message = f"{username}: {message}"
        client.send(message.encode())


# run receive_message in parrallel with send_message (main thread)
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

send_message()