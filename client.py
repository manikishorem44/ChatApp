# Class: CS544
# Date : 13 March, 2020
# Purpose: Implementing client logic 

from socket import AF_INET, socket, SOCK_STREAM  #python package for importing TCP sockets
from threading import Thread
import tkinter #python library for UI used in the chat
from datetime import datetime  #python package for datetime 
import time 
from hashlib import md5  #python package for hashcode

# STATEFUL

#Handles receiving of messages
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg = original_msg(msg)
            if msg =="{exit}":
                print("nvalid User/ Password")
                msg_list.insert(tkinter.END, "Invalid User/ Password")
                time.sleep(2) 
                client_socket.close()
                top.quit()
            msg_list.insert(tkinter.END, msg)
        except OSError: 
            break

#Handles sending of messages
def send(event=None):  
    raw_msg = my_msg.get() #reads the message from UI
    msg = add_header(raw_msg)
    my_msg.set("")  # Clears input field in UI.
    client_socket.send(bytes(msg, "utf8"))
    if raw_msg == "{exit}":
        client_socket.close()
        top.quit()

#Handles closing chat when user clicks close button in UI 
def on_closing(event=None):
    my_msg.set("{exit}")
    send()

#Adding Header
def add_header(raw_msg):
    version = '0'
    time = datetime.now().strftime("%H:%M:%S")
    msg_length = len(raw_msg)
    resv_bits = '8'
    msg_hash = handle_md5hash(raw_msg)
    msg = str(version)+'¦¦'+str(time)+'¦¦'+str(msg_length)+'¦¦'+str(resv_bits)+'¦¦'+str(raw_msg)+'¦¦'+str(msg_hash)
    return msg

#Seperating Header and message
def original_msg(h_msg):
    msg_n = h_msg.split('¦¦')
    return msg_n[len(msg_n)-2]

#Function that generates hash code for message
def handle_md5hash(msg):
    msg_hash = md5(msg.encode()).hexdigest()
    return msg_hash

# STATEFUL

# Implementing UI for protocol using python inbuilt package Tinker
top = tkinter.Tk()
top.title("Chat Screen")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # Creating a variable for handling messages in UI.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # Scroll bar to navigate.
# Handling messages in UI(Tinker).
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)

#UI part ends

# Requesting host IP from client
HOST = input('Enter host: ')  #CLIENT
# Port numer of server
PORT = 3300 


BUFSIZ = 1024
ADDR = (HOST, PORT)

# creating client socket
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
# Creating a thread for client
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop() #invoking UI for chat