import socket
import threading

Lock = threading.Lock() # Creating a lock object to avoid race conditions

Clients = [] # Creating a list to store the connection objects of clients

def client_handling(conn, addr):
    while True:
        text = conn.recv(1024) # Receives data from client, 1024 bytes at a time

        if not text:
            break

        print(f"Received from {addr}: {text.decode()}") # Prints the data received from the client after decoding it to string

        for client in Clients:
            if client != conn: # Sends data to all connected clients except the sender
                client.sendall(text) # Sends data to all connected clients after converting the same to bytes

def main():
    # Defining port number, host name, and header length
    HOST = 'localhost'
    PORT = 1250
    HEADER = 64

    s = socket.socket() # Creating the socket object and specifying the TCP/IP Protocol
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Eliminates "Address already in use" Error
    s.bind((HOST, PORT)) # Assigning specified IP Address and port number to the socket object
    s.listen() # Listens to client connection

    print(f"Connections made on {HOST} on port {PORT}")

    while True:
        conn, addr = s.accept() # Returns a tuple containing a connection object and the Port Number
        Lock.acquire() # Acquiring the lock to avoid race conditions
        thread1 = threading.Thread(target=client_handling, args=(conn, addr)) # Creating a thread to handle the client
        Clients.append(conn) # Appending the connection object to the Clients list
        thread1.start() # Starting the thread to handle the client
        Lock.release() # Releasing the lock after the thread has been created

        print(f"Connected to ", str(addr)) # Prints IP Address and port number to which client has connected

if __name__ == "__main__":   
    main() # Calling the main function to execute the code

# Create separate threads for sending and receiving messages
