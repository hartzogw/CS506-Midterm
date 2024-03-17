import socket,time



server_port = 8000

def run_client():
    time.sleep(5)
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "localhost"  # replace with the server's IP address

    # establish connection with server
    
    client.connect((server_ip, server_port))
    

    while True:
        # input message and send it to the server

        msg = input("Enter a new port number\n ")
        client.send(msg.encode("utf-8")[:1024])

        # receive message from the server
        response = client.recv(1024)
        response = response.decode("utf-8")

        # if server sent us "closed" in the payload, we break out of the loop and close our socket
        if response.lower() == "closed":
            break

    # close client socket (connection to the server)
    client.close()
    print("Connection to server closed")

run_client()
