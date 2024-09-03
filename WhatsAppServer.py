import dotenv
import os
import model.logger
import model.server

if __name__ == "__main__":
    dotenv.load_dotenv()
    logger = model.logger.logger

    whatsapp_port = int(os.getenv("WHATSAPP_PORT"))
    whatsapp_host = os.getenv("WHATSAPP_HOST")
    data_path = os.getenv("DATA_PATH")

    whatsapp_server = model.server.WhatsAppServer(whatsapp_host, whatsapp_port, data_path)
    logger.logger.info(f"Starting WhatsApp server on {whatsapp_host}:{whatsapp_port}")
    whatsapp_server.start()
