import socket
import threading

def broadcast(msg):
    # Send message to all client
    for client in clients:
        client.send(msg)

def handle_client(client_socket, addr, clients, names):
    try:
        while True:
            try:        
                # Receive and print client messages
                msg = client_socket.recv(1024)
                
                # Keyword to leave the chat
                if msg.lower() == 'closed':
                    print("\nGoodbye")
                    break
                
                # Send message to all client
                broadcast(msg)
            except:
                # Remove client from a list and let other know when they leave the chat
                idx = clients.index(client_socket)
                clients.remove(client_socket)
                client_socket.close()
                nickname = names[idx]
                names.pop(idx)
                msg = f"{nickname} left the chat!".encode("utf-8")
                broadcast(msg)
                break  
    finally:
        client_socket.close()

def run_server(port, names, thread):
    try:
        # Create server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the host and port
        server.bind((server_ip, port))
        
        # Listen for incoming connections
        server.listen(5)
        print(f"Listening on {server_ip}:{port}")
        
        while True:
            # Accept a client connection
            client_socket, addr = server.accept()
            print(f"\nAccepted connection from {addr[0]}:{addr[1]}\n")
            
            # Ask user for a nickname to use in chat
            client_socket.send('Nickname'.encode("utf-8"))
            nickname = client_socket.recv(1024).decode("utf-8")
            names.append(nickname)
            clients.append(client_socket)
            print(f"Name of the client is {nickname}")
            
            # Let other knows when someone joins a chat
            msg = f"{nickname} join the chat!".encode("utf-8")
            broadcast(msg)
            
            # Let user know that they are connected to the server
            client_socket.send('Connected to the server!'.encode("utf-8"))                        
            
            # Create thread for each client
            thread = threading.Thread(target=handle_client, args=(client_socket, addr, clients, names))
            thread.start()
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    clients = []
    names = []
    threads = []
    
    # Server hostname or IP address
    server_ip = "localhost"  
    
    # Create multiple server instances
    for port in [8080, 8081, 8082]:
        thread = threading.Thread(target=run_server, args=(port, names, threads))
        thread.start()
        threads.append(thread)
        
    for thread in threads:
        thread.join()
