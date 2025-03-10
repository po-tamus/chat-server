import socket
import threading 

HOST = "127.0.0.1"
PORT = 12345


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message): 
    for client in clients: 
        client.send(message)

def handle(client): 
    while True: 
        try: 
            message = client.recv(1024)
            broadcast(message)
        except: 
            print(f"failed...")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat".encode('ascii'))
            nicknames.remove(nickname)
            break 

def receive(): 
    while True: 
        # constantly accepting clients
        client, address = server.accept()
        print(f"Connected with {str(address)}") 

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the new client is {nickname}")
        broadcast(f"{nickname} joined the chat".encode('ascii'))
        client.send("connected to the server".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")

receive()
