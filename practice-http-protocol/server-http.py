import http.server
import socketserver

# -- IP and the port of the server
IP = "10.10.108.129"  # Localhost means "I": your local machine
PORT = 8002


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open("index.html", "r") as f:
                data = f.read()
                self.wfile.write(bytes(data, "utf8"))

            return
        
        elif "new" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            with open("new.html", "r") as f:
                file = f.read()
            self.wfile.write(bytes(file, "utf8"))
            
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("error.html", "r") as f:
                file = f.read()
            self.wfile.write(bytes(file, "utf8"))


# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass

httpd.server_close()
print("")
print("Server stopped!")


# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py