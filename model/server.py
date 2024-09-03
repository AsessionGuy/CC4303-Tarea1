"""
This module contains the HttpServer class and child classes
InstagramServer and WhatsappServer.
"""
import socket

from model.logger import logger
from model.query import InstagramQuery, WhatsAppQuery, Query
from model.request_handler import HttpRequestHandler, InstagramRequestHandler, WhatsAppRequestHandler, \
    SocialNetworkRequestHandler


class HttpServer:
    """
    A simple HttpServer class that listens on a port and returns a response.
    This class will be used as template for the other servers in the project.

    Attributes:
        host (str): The host to listen on.
        port (int): The port to listen on.
        http_request_handler (RequestHandler): The request handler to use.
        social_network_request_handler (SocialNetworkServerRequestHandler): The social network request handler to use.
        name (str): The name of the server.
        client_socket: a socket to serve as a client to contact other servers.
    """

    def __init__(self, host, port, name, data_path):
        self.host = host
        self.port = port
        self.http_request_handler = HttpRequestHandler(data_path)
        self.social_network_request_handler = SocialNetworkRequestHandler(data_path, "all", Query)
        self.name = name
        self.linked_servers = []
        self.client_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        """
        Method to start the server, listen on the port and handle requests.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            logger.logger.info(f"{self.name}: Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                with conn:
                    logger.logger.info(f"{self.name}: Connection from {addr} has been established.")
                    logger.logger.info(f"{self.name}: Handling request for {addr}.")

                    # Check if the request is valid and can be handled
                    query = self.http_request_handler.handle_request(conn, addr)
                    if query:
                        logger.logger.info(f"{self.name}: Query for {addr} is {query.social_network} query.")

                        # Match query type, if its Instagram or Whatsapp send to the respective server
                        match query:
                            case InstagramQuery():
                                instagram_server = next((server for server in self.linked_servers if server[0] == "InstagramServer"), None)
                                response = self.send_request(instagram_server, query)
                                conn.sendall(response)
                                conn.close()

                            case WhatsAppQuery():
                                whatsapp_server = next((server for server in self.linked_servers if server[0] == "WhatsAppServer"), None)
                                conn.sendall(f"""HTTP/1.1 302 Found\r\n")
                                Location: {whatsapp_server[1]}:{whatsapp_server[2]}/{query.names}/{query.last_name}\r\n""".encode())
                                conn.close()

                            case Query():
                                self.social_network_request_handler.handle_query(query, conn, addr)

                    else:
                        logger.logger.error(f"{self.name}: Query for {addr} is None.")
                        logger.logger.info(f"{self.name}: Closing connection for {addr}.")
                        conn.close()

    def link_server(self, name, host, port):
        """
        Method to link a server to another server.
        :param name: the name of the server to link to.
        :param host: the host of the server to link to.
        :param port: the port of the server to link to.
        """
        self.linked_servers.append((name, host, port))

    def send_request(self, server, query):
        """
        Method to send a request to another server.
        :param server: the server to send the request to.
        :param query: the query to send.
        """
        self.client_socket.connect((server[1], server[2]))
        request = f"GET /{query.social_network}/{"/".join(query.names) + "/" + "/".join(query.last_name)} HTTP/1.1\r\nHost: {server[1]}:{server[2]}\r\n\r\n"
        self.client_socket.sendall(request.encode())
        response = self.client_socket.recv(1024)
        self.client_socket.close()
        return response

class SocialNetworkServer(HttpServer):
    """
    SocialNetworkServer class that extends HttpServer class and provides the behavior
    for the social network servers.
    """
    def __init__(self, host, port, name, data_path, social_network):
        super().__init__(host, port, name, data_path)
        self.social_network = social_network
        self.request_handler = SocialNetworkRequestHandler(data_path, social_network, Query)

    def start(self):
        """
        Method to start the server, listen on the port and handle requests.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            logger.logger.info(f"{self.name}: Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                with conn:
                    logger.logger.info(f"{self.name}: Connection from {addr} has been established.")
                    logger.logger.info(f"{self.name}: Handling request for {addr}.")

                    # Check if the request is valid and can be handled
                    query = self.social_network_request_handler.handle_request(conn, addr)
                    if query:
                        logger.logger.info(f"{self.name}: Query for {addr} is {query.social_network} query.")
                        self.request_handler.handle_query(query, conn, addr)

                    else:
                        logger.logger.error(f"{self.name}: Query for {addr} is None.")
                        logger.logger.info(f"{self.name}: Closing connection for {addr}.")
                        conn.close()

class InstagramServer(SocialNetworkServer):
    """
    InstagramServer class that extends HttpServer class and provides a specific
    request handler for Instagram requests.
    """

    def __init__(self, host, port, data_path):
        super().__init__(host, port, "InstagramServer", data_path, "instagram")
        self.social_network_request_handler = InstagramRequestHandler(data_path)

class WhatsAppServer(SocialNetworkServer):
    """
    WhatsAppServer class that extends HttpServer class and provides a specific
    request handler for WhatsApp requests.
    """

    def __init__(self, host, port, data_path):
        super().__init__(host, port, "WhatsAppServer", data_path, "whatsapp")
        self.social_network_request_handler = WhatsAppRequestHandler(data_path)
