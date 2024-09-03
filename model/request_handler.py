"""

"""
from model.logger import logger
from model.parser import CSVParser
from model.query import HttpQuery, InstagramQuery, WhatsAppQuery, AllQuery, Query

import pathlib

class RequestHandler:
    """
    Base class to handle each request received by the server.

    Attributes:
        path (str): The path to the data file.
    """
    def __init__(self, path):
        self.path = path


    def get_data(self):
        """
        Method to get the data from the file.
        :return: The parsed data.
        """
        extension = pathlib.Path(self.path).suffix
        match extension:
            case ".csv":
                return CSVParser(self.path).parse_data()
            case _:
                raise ValueError("Invalid file extension. Only .csv files are supported.")

    def handle_request(self, conn, addr):
        """
        Method to handle the request received by the server.

        Args:
            conn (socket): The connection object.
            addr (tuple): The address of the client.
        """
        raise NotImplementedError("handle_request method is not implemented.")

class HttpRequestHandler(RequestHandler):
    """
    HttpRequestHandler class that extends RequestHandler class and provides a specific
    request handler for HTTP requests.
    """

    def handle_request(self, conn, addr):
        """
        Method to handle the request received by the server.

        Args:
            conn (socket): The connection object.
            addr (tuple): The address of the client.
        """
        request = conn.recv(1024).decode()
        request = request.split("\r\n")
        first_line = request[0]
        method, path, protocol = first_line.split(" ")
        if method == "GET":
            if path == "/":
                conn.sendall(b"""HTTP/1.1 200 OK\r\n\r\n""")
                return None
            query = HttpQuery(path[1:])
            return self.handle_query(query, conn, addr)
        else:
            conn.sendall(b"""HTTP/1.1 405 Method Not Allowed\r\n\r\n""")
            return None

    def handle_query(self, query, conn, addr):
        """
        Method to handle the Http query received by the server.
        :param query: the http query
        :param conn: the connection object
        :param addr: the address of the client
        :return: The query object.
        """
        match query.social_network:
            case "instagram":
                return InstagramQuery(query.names, query.last_name)
            case "whatsapp":
                return WhatsAppQuery(query.names, query.last_name)
            case "all":
                return AllQuery(query.names, query.last_name)
            case _:
                return Query(query.social_network, query.names, query.last_name)

class SocialNetworkRequestHandler(RequestHandler):
    """
    SocialNetworkRequestHandler class that extends RequestHandler class and provides a specific
    request handler for social network requests.

    Attributes:
        query_class (Query): The query class to use for the social network requests.
        cache (dict): The cache to store the results of the queries.
        social_network (str): The social network to search for.
    """
    def __init__(self, path, social_network, query_class):
        super().__init__(path)
        self.query_class = query_class
        self.cache = {}
        if social_network != "all":
            self.social_network = social_network
        else:
            self.social_network = "all"

    def get_data(self):
        return super().get_data()[self.social_network]

    def handle_query(self, query, conn, addr):
        """
        Method to handle the social network query received.

        :param query: the query object
        :param conn: the connection object
        :param addr: the address of the client
        """
        logger.logger.info(f"Searching for {query.names} {query.last_name} in {query.social_network} data.")
        response = ""
        data = self.get_data()
        cached_query = self.check_cache(query)
        if cached_query:
            logger.logger.info(f"Query for {query.names} {query.last_name} found in cache.")
            response = self.cache[cached_query]
        else:
            logger.logger.info(f"Query for {query.names} {query.last_name} not found in cache.")
            if query.social_network == "all":
                for social_network, data in data.items():
                    if tuple([" ".join(query.names), " ".join(query.last_name)]) in data:
                        if response == "":
                            response = """HTTP/1.1 200 OK\r\n\r\n"""
                        response += f"{social_network},{data[tuple([" ".join(query.names), " ".join(query.last_name)])]}\r\n"
            else:
                if tuple([" ".join(query.names), " ".join(query.last_name)]) in data:
                    response = f"""HTTP/1.1 200 OK\r\n\r\n{data[tuple([" ".join(query.names), " ".join(query.last_name)])]}"""
            self.add_to_cache(query, response)

        if response == "":
            response = """HTTP/1.1 404 Not Found\r\n\r\n"""
            conn.sendall(response.encode())

        else:
            conn.sendall(response.encode())

    def handle_request(self, conn, addr):
        """
        Method to handle the request received by the server when it's a single social network.

        Args:
            conn (socket): The connection object.
            addr (tuple): The address of the client.
        """
        request = conn.recv(1024).decode()
        request = request.split("\r\n")
        first_line = request[0]
        method, path, protocol = first_line.split(" ")
        path = path[1:].split("/")
        last_names = (path[-2], path[-1])
        names = path[1:-2]
        return self.query_class(names, last_names)

    def check_cache(self, query):
        """
        Method to check if the query is in the cache.

        :param query: the query to check.
        :return: True if the query is in the cache, False otherwise.
        """
        for cached_query in self.cache.items():
            if cached_query[0] == " ".join(query.names) + " ".join(query.last_name):
                return cached_query[1]
        return False

    def add_to_cache(self, query, response):
        """
        Method to add the query to the cache.
        :param query: the query to add.
        :param response: the response to the query to add.
        """
        if len(self.cache) == 0:
            self.cache[tuple([" ".join(query.names) + " ".join(query.last_name), 0])] = response
            return
        elif len(self.cache) < 10:
            latest_query = 0
            for cached_query in self.cache.items():
                if cached_query[1] > latest_query:
                    latest_query = cached_query[1]
            self.cache[tuple([" ".join(query.names) + " ".join(query.last_name), latest_query + 1])] = response
            return
        latest_query = 0
        for cached_query in self.cache.items():
            if cached_query[1] > latest_query:
                latest_query = cached_query[1]
        first_query = latest_query
        for cached_query in self.cache.items():
            if cached_query[1] < first_query:
                first_query = cached_query[1]
        self.cache.pop(first_query)
        self.cache[tuple([" ".join(query.names) + " ".join(query.last_name), latest_query + 1])] = response
        return

class InstagramRequestHandler(SocialNetworkRequestHandler):
    """
    InstagramRequestHandler class that extends RequestHandler class and provides a specific
    request handler for Instagram requests.
    """

    def __init__(self, path):
        super().__init__(path, "instagram", InstagramQuery)



class WhatsAppRequestHandler(SocialNetworkRequestHandler):
    """
    WhatsAppRequestHandler class that extends RequestHandler class and provides a specific
    request handler for WhatsApp requests.
    """

    def __init__(self, path):
        super().__init__(path, "whatsapp", WhatsAppQuery)

