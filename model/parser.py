"""
Parser that will read the input file and return the data in a structured format.
"""

class Parser:
    """
    Parser class that reads the input file and returns the data in a structured format.

    Attributes:
        filename (str): The name of the file to read.
        data (str): The data read from the file.
    """

    def __init__(self, filename):
        self.filename = filename
        self.data = self.read_file()

    def read_file(self):
        """
        Method to read the input file and return the data.
        :return: The data read from the file.
        """
        with open(self.filename, "r") as f:
            data = f.read()
        return data

    def parse_data(self):
        """
        Method to parse the data read from the file and return it in a structured format.
        :return: The parsed data.
        """
        raise NotImplementedError("parse_data method is not implemented.")

class CSVParser(Parser):
    """
    CSVParse class that extends Parser class and provides a specific
    parser for CSV files.
    """

    def parse_data(self):
        """
        Method to parse the data read from the CSV file and return it in a structured format.
        :return: The parsed data.
        """
        data = self.data.split("\n")
        parsed_data = {}
        for line in data:
            line = line.split(",")
            social_network_handler = line[-1]
            social_network = line[-2]
            last_names = [line[-4], line[-3]]
            names = line[:-4]
            full_name = tuple(names + last_names)
            if social_network not in parsed_data:
                parsed_data[social_network] = {}
            parsed_data[social_network][tuple(map(lambda x: x.lower(), full_name))] = social_network_handler
        return parsed_data