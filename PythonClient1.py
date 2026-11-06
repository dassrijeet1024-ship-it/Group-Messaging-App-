import socket
import threading

HOST = 'localhost'
PORT = 1250
HEADER = 64

#name = input("Enter your name: ") # Taking input from the user for their name

def start_client(): # Main thread for the client to send messages to the server
    f = socket.socket() # Creating the socket object and specifying the TCP/IP Protocol
    f.connect((HOST, PORT)) # Connecting to the server using the specified IP Address and port number

    name = input("Enter your name: ") # Taking input from the user for their name
    print(f"{name} has connected to the server")

    thread2 = threading.Thread(target=receive_messages, args=(f,)) # Creating a thread to receive messages from the server
    thread2.start() # Starting the thread to receive messages from the server

    while True:

        message = input(f"{name}: ") # Taking input from the user
        full_message = f"{name}: {message}" # Concatenating the name and message to send to the server
        if message.lower() == 'exit': # If the user types 'exit', the client will close the connection and exit
            f.close() # Closing the connection to the server           
            break

        f.sendall(full_message.encode()) # Sending the message to the server after encoding it to bytes

def receive_messages(f):
    
    while True:
        data = f.recv(1024) # Receiving data from the server, 1024 bytes at a time

        if not data:
            print("Server has closed the connection")
            f.close() # Closing the connection to the server
            break

        print(data.decode()) # Printing the data received from the server after decoding it to string

if __name__ == "__main__":
    start_client() # Calling the start_client function to execute the code