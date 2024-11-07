import socket
import threading

IP = "127.0.0.1"
PORT = 42069

while True:
    username = input("Enter your username: ")
    if username.strip():
        break
    else:
        print("Username cannot be empty. Please try again.")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((IP, PORT))
except socket.error as e:
    print(f"Error connecting to server: {e}")
    exit(1)

message = f"---{username} entered the chat---"
try:
    client.send(message.encode())
except socket.error as e:
    print(f"Error sending message to server: {e}")
    client.close()
    exit(1)

def receive_message():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print("\r", message)
                print(f"\r{username}: ", end="")
        except socket.error as e:
            print("\rError receiving message from server:", e)
            client.close()
            break
        except Exception as e:
            print("\rUnexpected error receiving message:", e)
            client.close()
            break

def send_message():
    while True:
        message = input(f"{username}: ")
        message = f"{username}: {message}"
        try:
            client.send(message.encode())
        except socket.error as e:
            print(f"Error sending message to server: {e}")
            client.close()
            break
        except Exception as e:
            print(f"Unexpected error sending message: {e}")
            client.close()
            break

# Run receive_message in parallel with send_message (main thread)
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

send_message()