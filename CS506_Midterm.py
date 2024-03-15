from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import socket

#Create server instances
def run_server(port):
  server_address = ("", port)
  httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
  print(f"Server instance started at port {port}\n")
  httpd.serve_forever()

def check_server(address):
  try:
    response = requests.get(address + '/health', timeout=1)
    if response.status_code == 200:
      return True
    else:
      return False
  except:
    return False

#find a server
def find_server():
  if check_server:
    return check_server()
  return None

# Start servers using threading
threads = []
for port in [8080, 8081, 8082]:
  thread = threading.Thread(target=run_server, args=(port,))
  threads.append(thread)
  thread.start()
  
for thread in threads:
  thread.join()
