"""
This module contains the Query class. This class is used to store the information
about the query to be made to the social networks.
"""

class Query:
    """
    Base Query class for the model. Each query contains which social network it is for,
    the names and the last name of the person to search for.

    Attributes:
        social_network (str): The social network to search for.
        names (str): The first name of the person to search for.
        last_name (str): The last name of the person to search
    """

    def __init__(self, social_network, names, last_name):
        self.social_network = social_network
        self.names = names
        self.last_name = last_name

    def __str__(self):
        return f"{self.social_network}: {self.names} {self.last_name}"

class HttpQuery(Query):
    """
    HttpQuery class that extends Query class and provides a specific
    query for HTTP requests. This will be later used to differentiate
    between the different social networks.
    """

    def __init__(self, query):
        query = query.split("/")
        social_network = query[0]
        last_names = (query[-2], query[-1])
        names = query[1:-2]
        super().__init__(social_network, names, last_names)

class InstagramQuery(Query):
    """
    InstagramQuery class that extends Query class and provides a specific
    query for Instagram requests.
    """

    def __init__(self, names, last_name):
        super().__init__("instagram", names, last_name)

class WhatsAppQuery(Query):
    """
    WhatsAppQuery class that extends Query class and provides a specific
    query for WhatsApp requests.
    """

    def __init__(self, names, last_name):
        super().__init__("whatsapp", names, last_name)

class AllQuery(Query):
    """
    AllQuery class that extends Query class and provides a specific
    query for all social networks requests.
    """

    def __init__(self, names, last_name):
        super().__init__("all", names, last_name)