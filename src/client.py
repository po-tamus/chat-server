import socket
import threading 

HOST = "127.0.0.1"
PORT = 12345

nickname = input("choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT)) 

def receive(): 
    while True: 
        try: 
            message = client.recv(1024).decode('ascii')
            if message == "NICK": 
                client.send(nickname.encode('ascii'))
            else: 
                print(message)
        except: 
            print("an error occurred")
            client.close()
            break

def write(): 
    while True: 
        message = f"{nickname}: {input("")}" 
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
