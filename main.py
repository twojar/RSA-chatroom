import socket
import threading
import rsa

#CONSTANTS
#CHANGE IPV4_ADDRESS to YOUR IPV4 ADDRESS!!!!!
IPV4_ADDRESS = "ADD ADDRESS HERE"
PORT = 9999

#RSA Keys
public_key, private_key = rsa.newkeys(1024)
public_partner = None


choice = input("Select to either host (1) or connect (2)")

#create an internet socket
if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IPV4_ADDRESS, PORT))
    server.listen()

    #communication to client
    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IPV4_ADDRESS, 9999))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))

def send_messages(client):
    while True:
        message = input("")
        client.send(rsa.encrypt(message.encode(), public_partner))
        print("You: " + message)

def receive_messages(client):
    while True:
        print("Partner: " + rsa.decrypt(client.recv(1024), private_key).decode(encoding="utf-8", errors="strict"))

threading.Thread(target=send_messages, args=(client,)).start()
threading.Thread(target=receive_messages, args=(client,)).start()

