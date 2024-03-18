import socket
import threading 

def receive(client, name):
    while True:
        try:
            # Message recieves from server
            msg = client.recv(1024).decode("utf-8")
            if msg == 'Nickname':
                client.send(name.encode("utf-8"))            
            else:
                print(msg)
        except:
            print("Server shuts down!")
            client.close()
            break

def write(client, name):
    while True:
        # Get user input
        msg = input("")
        
        # Keyword to leave the chat
        if msg.lower() == 'closed':
            print("\nGoodbye")
            client.close()
            break
        
        # Send message to server
        msg =f'{name}: {msg}'        
        client.send(msg.encode("utf-8"))
           
def run_client():
    # Let user select the server
    while True:
        print("\nAvailable Port Numbers: 8080, 8081, 8082")
        print("Enter Port Number: ")
        msg = input("")
        
        # Check user input
        if msg == '8080' or msg == '8081' or msg =='8082':
            break
        else:
            print("\nInvalid Port!")
    
    # Server hostname or IP address
    server_ip = "localhost"  
    server_port = int(msg)
    name = input("Enter a nickname: ")
    
    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Establish connection with server
    client.connect((server_ip, server_port))
    
    # Start thread for recieving message    
    receive_thread = threading.Thread(target=receive, args=(client, name))
    receive_thread.start()
    
    # Start thread to send message
    write_thread = threading.Thread(target=write, args=(client, name))
    write_thread.start()

if __name__ == "__main__":
    run_client()
