import http.server
import socketserver
import json
import subprocess
from urllib.parse import urlparse
from urllib.parse import parse_qs

PORT = 8000
MODELPATH = "/models"

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        self.send_header("Content-type", "application/json")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        # prepare response
        response = { "status": 0, "message": "" }

        # Extract query param
        input = ''
        query_components = parse_qs(urlparse(self.path).query)
        if 'input' in query_components:
            input = query_components["input"][0]
        
        if len(input) <= 0:
            response["status"] = -1
            response["message"] = "invalid input"
            self.wfile.write(bytes(json.dumps(response), "utf8"))
            return

        response["status"], response["message"] = subprocess.getstatusoutput("deepspeech --model {}/deepspeech-0.9.3-models.pbmm --scorer {}/deepspeech-0.9.3-models.scorer --audio {}".format(MODELPATH, MODELPATH, input))
        self.wfile.write(bytes(json.dumps(response), "utf8"))
        return

# Create an object of the above class
handler_object = MyHttpRequestHandler
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Star the server
my_server.serve_forever()
