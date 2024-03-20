import socket
import threading

ADDRESSES = [("localhost", 8080), ("localhost", 8081), ("localhost", 8082)]

def check_servers(address, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((address, port))
        return True
    except:
        return False


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
        try:
            # Get user input
            msg = input("")

            # Keyword to leave the chat
            if msg.lower() == 'closed':
                print("\nGoodbye")
                client.close()
                break

            # Send message to server
            msg = f'{name}: {msg}'
            client.send(msg.encode("utf-8"))
        except:
            print("Server shuts down!")
            client.close()
            break


def run_client():
    server_ports = [8080, 8081, 8082]
    server_ips = ["localhost", "localhost", "localhost"]

    # Let user select the server
    while True:
        print("Available ports: ")
        for port in server_ports:
            print(port)
        print("Enter Port Number: ")
        msg = int(input(""))

        # Check user input
        if msg in server_ports:
            break
        else:
            print("\nInvalid Port!")

    # Server hostname or IP address

    name = input("Enter a nickname: ")


    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Establish connection with server
    try:
        #if check_servers(server_ips[0], msg):
        client.connect((server_ips[0], msg))
    except ConnectionRefusedError:
        print("Connection refused! Trying other available ports...")
        try:
            client.connect((server_ips[0], 8081))
        except ConnectionRefusedError:
            print("Connection refused! Trying other available ports...")
            try:
                client.connect((server_ips[0], 8082))
            except ConnectionRefusedError:
                print("No available ports!")


    except ConnectionAbortedError:
        print("Connection was aborted!")

    # Start thread for recieving message
    receive_thread = threading.Thread(target=receive, args=(client, name))
    receive_thread.start()

    # Start thread to send message
    write_thread = threading.Thread(target=write, args=(client, name))
    write_thread.start()


if __name__ == "__main__":
    run_client()