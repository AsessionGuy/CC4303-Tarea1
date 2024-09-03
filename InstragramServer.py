import dotenv
import os
import model.server
import model.logger

if __name__ == "__main__":
    dotenv.load_dotenv()
    logger = model.logger.logger

    instagram_port = int(os.getenv("INSTAGRAM_PORT"))
    instagram_host = os.getenv("INSTAGRAM_HOST")
    data_path = os.getenv("DATA_PATH")

    instagram_server = model.server.InstagramServer(instagram_host, instagram_port, data_path)
    logger.logger.info(f"Starting Instagram server on {instagram_host}:{instagram_port}")
    instagram_server.start()