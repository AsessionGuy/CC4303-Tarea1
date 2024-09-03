"""
This is the main file of the project. It will check for the creation of the servers.
"""
import dotenv
import socket
import os

def wait_for_server(host, port, name):
    """
    Function to wait for the server to be created.
    :param name: the name of the server.
    :param host: the host of the server.
    :param port: the port of the server.
    """
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                request = f"GET / HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n"
                s.sendall(request.encode())

                response = s.recv(1024)
                if response:
                    print(f"\r{name} server is up and running on {host}:{port}")
                    break
        except:
            print(f"\rWaiting for {name} Server", end="")

if "__main__" == __name__:

    # Load environment variables
    dotenv.load_dotenv()

    # get the host and port of the servers
    instagram_host = os.getenv("INSTAGRAM_HOST")
    instagram_port = int(os.getenv("INSTAGRAM_PORT"))
    whatsapp_host = os.getenv("WHATSAPP_HOST")
    whatsapp_port = int(os.getenv("WHATSAPP_PORT"))
    http_host = os.getenv("HTTP_HOST")
    http_port = int(os.getenv("HTTP_PORT"))

    # wait for the servers to be created
    wait_for_server(instagram_host, instagram_port, "Instagram")
    wait_for_server(whatsapp_host, whatsapp_port, "WhatsApp")
    wait_for_server(http_host, http_port, "Http")

    print("All servers are up and running. Ready to accept requests.")