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

    thread2 = threading.Thread(target=receive_messages, args=(f, name)) # Creating a thread to receive messages from the server
    thread2.daemon = True # Setting the thread as a daemon thread so that it will exit when the main thread exits
    thread2.start() # Starting the thread to receive messages from the server

    while True:

        message = input(f"{name}: ") # Taking input from the user
        if message.lower() == 'exit': # If the user types 'exit', the client will close the connection and exit
            f.close() # Closing the connection to the server           
            break

        full_message = f"{name}: {message}" # Concatenating the name and message to send to the server


        f.sendall(full_message.encode()) # Sending the message to the server after encoding it to bytes

def receive_messages(f, name):
    
    while True:

        try:
            data = f.recv(1024) # Receiving data from the server, 1024 bytes at a time

            if not data: # If no data is received, it means the server has closed the connection
                print("Server has closed the connection.")
                break

            with threading.Lock(): # Using a lock to prevent multiple threads from printing at the same time
                print(data.decode()) # Printing the data received from the server after decoding it to string

                print(f"{name}: ", end='', flush=True) # Printing the user's name and a prompt for input without a newline
    
        except Exception as e:
            print(f"An error occurred: {e}") # Printing any exceptions that occur during receiving messages
            break

if __name__ == "__main__":
    start_client() # Calling the start_client function to execute the code