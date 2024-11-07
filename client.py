import socket
import threading
import ssl
import sys

IP = "127.0.0.1"
PORT = 42069
while True:
    username = input("Enter your username: ")
    if username.strip():
        break
    else:
        print("Username cannot be empty. Please try again.")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

context = ssl.create_default_context()
context.check_hostname = False 
context.verify_mode = ssl.CERT_NONE 

ssl_client = context.wrap_socket(client)

try:
    ssl_client.connect((IP, PORT))
except socket.error as e:
    print(f"Error connecting to server: {e}")
    sys.exit(1)

message = f"---{username} entered the chat---"
try:
    ssl_client.send(message.encode())
except socket.error as e:
    print(f"Error sending message to server: {e}")
    ssl_client.close()
    sys.exit(1)

def receive_message():
    while True:
        try:
            message = ssl_client.recv(1024).decode()
            if message:
                print("\r", message)
                print(f"\r{username}: ", end="")
            else:
                print("\rConnection closed by the server.")
                ssl_client.close()
                break
        except socket.error as e:
            print("\rError receiving message from server:", e)
            ssl_client.close()
            break
        except Exception as e:
            print("\rUnexpected error receiving message:", e)
            ssl_client.close()
            break

def send_message():
    while True:
        message = input(f"{username}: ")
        message = f"{username}: {message}"
        try:
            ssl_client.send(message.encode())
        except socket.error as e:
            print(f"Error sending message to server: {e}")
            ssl_client.close()
            break
        except Exception as e:
            print(f"Unexpected error sending message: {e}")
            ssl_client.close()
            break

# run receive_message in a separate thread
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

# run send_message in the main thread
send_message()