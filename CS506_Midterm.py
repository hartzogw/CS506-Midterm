from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading


#Create server instances
def run_server(port):
  server_address = ("", port)
  httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
  print(f"Server instance started at port {port}\n")
  httpd.serve_forever()

# Start servers using threading
threads = []
for port in [8080, 8081, 8082]:
  thread = threading.Thread(target=run_server, args=(port,))
  threads.append(thread)
  thread.start()
  
for thread in threads:
  thread.join()
