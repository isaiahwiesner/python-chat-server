import socket
import threading

HOST = "127.0.0.1" # localhost IP
# HOST = "10.16.26.156" # private IP
#   connect to 142.55.3.15
PORT = 9090

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# List of clients
clients = []

# List of nicknames
nicknames = []

# Broadcast
def broadcast(message):
    for client in clients:
        client.send(message)

# Receive
def receive():
    while True:
        client, address = server.accept()
        print(f'Client connected with {str(address)}!')
        
        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")
        
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client connected with {str(address)} is {nickname}')
        broadcast(f'{nickname} has connected to the server!\n'.encode("utf-8"))
        client.send("Connected to the server!".encode("utf-8"))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Handle
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f'{nicknames[clients.index(client)]} says {message}')
            broadcast(message)
        except:
            i = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[i]
            nicknames.remove(nickname)
            broadcast(f'{nickname} has disconnected from the server.'.encode("utf-8"))
            break

if __name__ == "__main__":
    print(f'Server running on (\'{HOST}\', {PORT})')
    receive()