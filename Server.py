"""An example of a simple HTTP server."""
from __future__ import print_function

import mimetypes
import socket
import subprocess
import json

try:
    from urllib.parse import unquote_plus
except ImportError:
    from urllib import unquote_plus

# Header template for a successful HTTP request
HEADER_RESPONSE_200 = """HTTP/1.1 200 OK
content-type: %s
content-length: %d
connection: Close

"""

# Template for a 404 (Not found) error
RESPONSE_404 = """HTTP/1.1 404 Not found
content-type: text/html
connection: Close

<!doctype html>
<h1>404 Page not found</h1>
<p>Page cannot be found.</p>
"""


def extract_headers (file_input):
    headers = {}
    while True:
        line = file_input.readline().strip()
        if line == "":
            break
        key,value = line.split(": ")
        headers[key] = value
    return headers

def Get_parse (tekst):
    parametri = {}
    for sprem in tekst.split("&"):
        key,value = sprem.split("=")
        parametri[key] = value
    return parametri


def process_request(connection, address):
    """Process an incoming socket request.

    :param connection is a socket of the client
    :param address is a 2-tuple (address(str), port(int)) of the client
    """
    file_input = connection.makefile()

    # Read one line

    line = file_input.readline().strip()
    if line == '':
        return



    # Read and parse the request line
    try:
        method, filename, version = line.split()
    except ValueError:
        connection.sendall(RESPONSE_404.encode("utf-8"))
        return
    if method != "GET" and method != "POST" or filename == "" or version != "HTTP/1.1" :
        connection.sendall(RESPONSE_404.encode("utf-8"))
        return
    filename = filename[1:]


    # Read and parse headers
    headers = extract_headers(file_input)
    Params = {}
    if "?" in filename:
        nameAndParams = filename.split("?")
        filename = nameAndParams[0]
        Params = Get_parse (unquote_plus(nameAndParams[1]))

    filenameF = "strani/" + filename

    if "cron" in filenameF:
        subprocess.Popen(["python", "server_side/get_Events_from_dars.py"])
        filenameF = filenameF.replace("cron", "cron.html")
        with open(filenameF, "rb") as handle:
            response_body = handle.read()
        type_, _ = mimetypes.guess_type(filename)
        if type_ == "None":
            type_ = "application/octet-stream"
        response_header = HEADER_RESPONSE_200 % (type_, len(response_body))
        connection.sendall(response_header.encode("utf-8"))
        connection.sendall(response_body)

    elif "events" in filenameF:
        if ".js" not in filenameF:
            # preberi json iz datoteke
            dat = open("server_side/dogodki_dars.txt","r")
            dogodkiJ = dat.read()
            filenameF = filenameF.replace("events", "events.html")
            with open(filenameF, "rb") as handle:
                response_body = handle.read()
            #dodaj json in parametre v onload="populateDiv()"
            parametri = json.dumps(Params)
            response_body = response_body.replace(b"{{dogodki}}", bytes(dogodkiJ,"utf-8"))
            response_body = response_body.replace(b"{{argumenti}}",bytes(parametri,"utf-8"))

            type_, _ = mimetypes.guess_type(filename)
            if type_ == "None":
                type_ = "application/octet-stream"
            response_header = HEADER_RESPONSE_200 % (type_, len(response_body))
            connection.sendall(response_header.encode("utf-8"))
            connection.sendall(response_body)
        else:
            with open(filenameF, "rb") as handle:
                response_body = handle.read()
            type_, _ = mimetypes.guess_type(filename)
            if type_ == "None":
                type_ = "application/octet-stream"
            response_header = HEADER_RESPONSE_200 % (type_, len(response_body))
            connection.sendall(response_header.encode("utf-8"))
            connection.sendall(response_body)


def main(port):
    """Starts the server and waits for connections."""

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", port))
    server.listen(1)

    print("Listening on %d" % port)

    while True:
        connection, address = server.accept()
        print("[%s:%d] CONNECTED" % address)
        process_request(connection, address)
        connection.close()
        print("[%s:%d] DISCONNECTED" % address)


if __name__ == "__main__":
    main(8080)
