import socket,threading
import serverchoice 



server_ip = "localhost"  # server hostname or IP address
port = int(serverchoice.msg)  # server port number


#check current server status
def check_server(address):
  try:
    response = requests.get(address + '/health', timeout=1)
    if response.status_code == 200:
      print(f"Server at {address} is operational.")
      return True
    else:
      print(f"Server at {address} is not operational.")
      return False
  except:
    print(f"Server at {address} cannot be validated.")
    return False


  # find a server from a list of all current active servers
  def find_server():
      for server in servers:
          if check_server(server):
              return server
          return None


def handle_client(client_socket, addr):
    try:
        while True:
            #checking the validity of the server before each request
            if not check_server(addr):
                addr = find_server()
            else:
                break

            # receive and print client messages
            request = client_socket.recv(1024).decode("utf-8")
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break
            print(f"Received: {request}")

            # convert and send accept response to the client
            response = request.encode("utf-8")
            client_socket.send(response)
            client_socket.detach()
            changedport = int(request)
            print(f"{addr[0]}:{addr[1]}) changed port to: {changedport}")

            print(f"Now listening on {server_ip}:{changedport}")

    except Exception as e:
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def run_server(port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind the socket to the host and port
        server.bind((server_ip, port))

        # listen for incoming connections
        server.listen(5)
        print(f"Listening on {server_ip}:{port}")

        # accept a client connection
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}\n")
        working_server = find_server()

        # start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
        thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()

run_server(port)
