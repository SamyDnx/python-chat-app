import sys
import socket
import threading

IP = "127.0.0.1"
PORT = 42069

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

username = input("Enter your usename: ")

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
            sys.exit()

def send_message():
    while True:
        message = input(username + ": ")
        message = f"{username}: {message}"
        client.send(message.encode())


# run receive_message in parrallel with send_message (main thread)
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

send_message()