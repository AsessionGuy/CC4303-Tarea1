import dotenv
import os
import model.logger
import model.server

if __name__ == "__main__":
    dotenv.load_dotenv()
    logger = model.logger.logger

    http_port = int(os.getenv("HTTP_PORT"))
    http_host = os.getenv("HTTP_HOST")
    data_path = os.getenv("DATA_PATH")

    http_server = model.server.HttpServer(http_host, http_port, "HttpServer", data_path)
    http_server.link_server("InstagramServer", os.getenv("INSTAGRAM_HOST"), int(os.getenv("INSTAGRAM_PORT")))
    http_server.link_server("WhatsAppServer", os.getenv("WHATSAPP_HOST"), int(os.getenv("WHATSAPP_PORT")))
    logger.logger.info(f"Starting HTTP server on {http_host}:{http_port}")
    http_server.start()
