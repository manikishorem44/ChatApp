# Class: CS544
# Date : 13 March, 2020
# Purpose: Implementing Server logic

from socket import AF_INET, socket, SOCK_STREAM  #python package for importing TCP sockets
from threading import Thread
from datetime import datetime  #python package for datetime 
from hashlib import md5  #python package for hashcode

#STATEFUL
#handles incoming connections
def accept_connection():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Enter you user name", "utf8"))
        name = client.recv(BUFSIZ).decode("utf8")
        name = original_msg(name)
        client.send(bytes("Enter password", "utf8"))
        password = client.recv(BUFSIZ).decode("utf8")
        password = original_msg(password)
        # Handling User Authentication 
        if (name == "Mani" and password == "Mani@123" or name == "Kishore" and password == "Kishore@123" or
              name == "Aditya" and password == "Aditya@123" or name == "Likil" and password == "Likil@123" or 
               name == "Pradeep" and password == "Pradeep@123"  ):
            client.send(bytes(" Authorization Success", "utf8"))
            print("join")
            addresses[client] = client_address   #Saving client address in a list
            Thread(target=handle_client, args=(client, name, )).start() #starting a thread once authentication is done
        else:   
            client.send(bytes("{exit}", "utf8"))
            client.close()

# Handles every single client connection 
#Takes client socket as input argument
#It starts once authentication is done
def handle_client(client, name):  
    welcome = 'Welcome %s! If you want to exit type {exit}.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(msg)
    clients[client] = name
   #Handles Chat 
    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        msg = original_msg(msg)
        #Broadcasts message to all the clients in the chat
        if msg != "{exit}":
            broadcast(msg, name+": ")
        #Handles exit messages from client
        else:
            print("left")
            client.send(bytes("{exit}", "utf8"))
            client.close()
            del clients[client]
            broadcast("%s has left the chat." % name)
            break

# Broadcast takes two arguments, message and name of client as prefix 
# It will broadcast message to all clients in the chat
def broadcast(msg, prefix=""):  
    """Broadcasts a message to all the clients."""
    msg = prefix+str(msg)
    msg = add_header(msg)
    for sock in clients:
        sock.send(bytes(msg, "utf8"))

#handles adding header mechanism to message
def add_header(raw_msg):
    version = '0'
    time = datetime.now().strftime("%H:%M:%S")
    msg_length = len(raw_msg)
    resv_bits = '8'
    msg_hash = handle_md5hash(raw_msg)
    msg = str(version)+'¦¦'+str(time)+'¦¦'+str(msg_length)+'¦¦'+str(resv_bits)+'¦¦'+str(raw_msg)+'¦¦'+str(msg_hash)
    return msg

#Handles seperating original message from header
#Performs Error checking
def original_msg(h_msg):
    msg_n = h_msg.split('¦¦')
    msg_hash = msg_n[len(msg_n)-1]
    # print("original hash", msg_hash)
    msg_hash_new = handle_md5hash(msg_n[len(msg_n)-2])
    # print("hash at server", msg_hash_new)
    if msg_hash == msg_hash_new:
        print('Success')
        return msg_n[len(msg_n)-2]
    else:
        return ("Msg got corrupted, Resend message")

#Function that generates hash code for message
def handle_md5hash(msg):
    msg_hash = md5(msg.encode()).hexdigest()
    return msg_hash

#STATEFUL

#Empty lists to store client objects and addresses      
clients = {}
addresses = {}

HOST = ''
PORT = 3300 #SERVICE
BUFSIZ = 1024
ADDR = (HOST, PORT)

#creating Socket and binding it to address
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

#Execution starts from here

if __name__ == "__main__":
    SERVER.listen(5) #listens for maximum of 5 clients 
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connection) #starts a thread #CONCURRENT
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()