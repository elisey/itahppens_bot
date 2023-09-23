import logging

from app.bot import Bot
from app.core.config import settings
from app.quotes_client.http_client import QuotesClientHttp


logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.ERROR)


def main() -> None:
    try:
        quote_service_client = QuotesClientHttp(settings.quote_service_url)
        bot = Bot(quote_service_client)
        bot.run()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        logging.info("Application ended")


if __name__ == "__main__":
    main()
